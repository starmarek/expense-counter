<template>
    <div class="m-5">
        <b-table :data="bankStatementData" paginated :per-page="perPage">
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
                centered
                v-slot="props"
                width="100"
            >
                {{ props.row.name }}
            </b-table-column>
            <b-table-column field="note" label="Note" v-slot="props" width="100">
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
            <b-table-column field="date" label="Date" sortable v-slot="props">
                {{ props.row.date }}
            </b-table-column>
            <b-table-column field="actions" label="Actions" v-slot="props">
                <span>
                    <b-button
                        size="is-small"
                        type="is-link"
                        icon-left="download"
                        @click="downloadFile(props.row.id)"
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
            <!-- <pdf src="../../../backend/bank_statement/store/3.pdf"></pdf> -->
            <!-- <a href="../../../backend/bank_statement/store/3.pdf" target="_blank"
                >HTML a href target _blank</a
            > -->
        </b-table>
    </div>
</template>

<script>
import bankStatementService from "@/services/bankStatementService";
import { mapActions, mapState, mapMutations } from "vuex";
// import pdf from "vue-pdf";
export default {
    data() {
        return {
            perPage: 25,
            // isLoaded: false,
        };
    },
    created() {
        var fetchData = { ordering: "-id", user: this.chosenUser.id };
        this.getBankStatements(fetchData)
            .then(() => {
                // this.isLoaded = false;
            })
            .catch(() => {
                this.$buefy.notification.open({
                    duration: 5000,
                    message:
                        "Unable to load data from database, check internet connection.",
                    type: "is-danger",
                });
            });
    },
    computed: {
        ...mapState("bank_statement", ["bankStatementData"]),
        ...mapState("user", ["chosenUser"]),
    },
    // components: {
    //     pdf,
    // },
    methods: {
        ...mapActions("bank_statement", ["getBankStatements"]),
        ...mapMutations("user", ["setChosenUser"]),
        loadAsyncData() {
            // this.isLoaded = true;
        },
        deleteFile(idx) {
            bankStatementService
                .deleteStatement(idx)
                .then(() => {
                    this.$buefy.notification.open({
                        duration: 2000,
                        message: "Statement was deleted.",
                        type: "is-success",
                    });
                })
                .catch((error) => {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: error,
                        type: "is-danger",
                    });
                });
            this.loadAsyncData();
        },
        downloadFile(idx) {
            bankStatementService
                .downloadStatement(idx)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        previewFile(idx) {
            bankStatementService
                .previewStatement(idx)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>

<style></style>
