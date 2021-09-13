<template>
    <span class="centerTable">
        <b-field grouped group-multiline>
            <b-button
                label="Clear checked"
                type="is-link is-light"
                icon-left="close"
                class="field"
                @click="checkedRows = []"
            />
            <b-button
                label="Delete selected"
                type="is-danger"
                icon-left="delete"
                class="field"
                @click="deleteChosenFiles"
            />
            <b-button
                label="Refresh page"
                type="is-link"
                icon-left="refresh"
                class="field"
                @click="loadAsync"
            />
        </b-field>
        <b-table
            :data="bankStatementData"
            paginated
            :per-page="perPage"
            hoverable
            :checked-rows.sync="checkedRows"
            checkable
        >
            <b-table-column
                field="id"
                label="ID"
                numeric
                sortable
                centered
                v-slot="props"
                width="40"
            >
                {{ props.row.id }}
            </b-table-column>
            <b-table-column
                field="name"
                label="Name"
                sortable
                v-slot="props"
                word-break="break-word"
            >
                {{ props.row.name }}
            </b-table-column>
            <b-table-column field="note" label="Note" v-slot="props">
                {{ props.row.note }}
            </b-table-column>
            <b-table-column
                field="date_upload"
                label="Upload date"
                sortable
                centered
                v-slot="props"
            >
                {{ props.row.date_upload }}
            </b-table-column>
            <b-table-column
                field="date"
                label="Statement date"
                sortable
                centered
                v-slot="props"
            >
                {{ props.row.date }}
            </b-table-column>
            <b-table-column field="actions" label="Actions" v-slot="props" centered>
                <span>
                    <b-button
                        size="is-small"
                        type="is-link"
                        icon-left="download"
                        @click="downloadFile(props.row.id, props.row.name)"
                    >
                        Download
                    </b-button>
                    <b-button
                        size="is-small"
                        type="is-success"
                        icon-left="eye"
                        @click="previewFile(props.row.id)"
                    >
                        Preview
                    </b-button>
                    <b-button
                        size="is-small"
                        type="is-danger"
                        icon-left="delete"
                        @click="deleteFile(props.row.id)"
                    >
                        Delete
                    </b-button>
                </span>
            </b-table-column>
        </b-table>
    </span>
</template>

<script>
import bankStatementService from "@/services/bankStatementService";
import { mapActions, mapState, mapMutations } from "vuex";
export default {
    data() {
        return {
            perPage: 5,
            checkedRows: [],
        };
    },
    created() {
        this.loadAsync();
    },
    computed: {
        ...mapState("bank_statement", ["bankStatementData"]),
        ...mapState("user", ["chosenUser"]),
    },
    methods: {
        ...mapActions("bank_statement", ["getBankStatements"]),
        ...mapMutations("user", ["setChosenUser"]),
        loadAsync() {
            var fetchData = { ordering: "-id", user: this.chosenUser.id };
            this.getBankStatements(fetchData).catch(() => {
                this.$buefy.notification.open({
                    duration: 3000,
                    message:
                        "Unable to load data from database, check internet connection.",
                    type: "is-danger",
                });
            });
        },
        async deleteFile(idx) {
            await bankStatementService
                .deleteStatement(idx)
                .then(() => {
                    this.$buefy.notification.open({
                        duration: 2000,
                        message: "Statement was deleted.",
                        type: "is-info",
                    });
                    this.loadAsync();
                })
                .catch((error) => {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: error,
                        type: "is-error",
                    });
                });
        },
        downloadFile(idx, name) {
            bankStatementService
                .getPdfStatement(idx)
                .then((response) => {
                    let blob = new Blob([response], { type: "application/pdf" });
                    const blobUrl = URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = blobUrl;
                    link.download = name;
                    document.body.appendChild(link);
                    link.dispatchEvent(
                        new MouseEvent("click", {
                            bubbles: true,
                            cancelable: true,
                            view: window,
                        })
                    );
                    document.body.removeChild(link);
                })
                .catch((error) => {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: error,
                        type: "is-danger",
                    });
                });
        },
        previewFile(idx) {
            bankStatementService
                .getPdfStatement(idx)
                .then((response) => {
                    let blob = new Blob([response], { type: "application/pdf" });
                    const url = window.URL.createObjectURL(blob);
                    window.open(url, "_blank");
                })
                .catch((error) => {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: error,
                        type: "is-danger",
                    });
                });
        },
        deleteChosenFiles() {
            for (const x of this.checkedRows) {
                this.deleteFile(x.id);
            }
            this.checkedRows = [];
        },
    },
};
</script>

<style>
.centerTable {
    width: 100%;
    margin: 1.5rem;
}
</style>
