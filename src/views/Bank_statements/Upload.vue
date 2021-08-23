<template>
    <div class="modal-card" style="width: 400px">
        <header class="modal-card-head">
            <p class="modal-card-title">Upload your statement as PDF</p>
        </header>
        <section class="modal-card-body">
            <b-field>
                <b-upload v-model="dropFiles" multiple drag-drop>
                    <section class="section">
                        <div class="content has-text-centered">
                            <p>
                                <b-icon icon="upload" size="is-large"></b-icon>
                            </p>
                            <p>Drop your statements here or click to upload</p>
                        </div>
                    </section>
                </b-upload>
            </b-field>

            <div>
                <span
                    v-for="(file, index) in dropFiles"
                    :key="index"
                    class="tag is-info"
                >
                    {{ file.name }}
                    <button
                        class="delete is-small"
                        type="is-link"
                        @click="deleteDropFile(index)"
                    ></button>
                </span>
            </div>
        </section>
        <footer class="modal-card-foot">
            <b-button label="Close" @click="$parent.close()" />
            <!-- <b-button class="button" @click="addNote">
                <span>{{ "Add notes" }}</span>
            </b-button> -->
            <div v-if="loading">
                <button class="button is-link is-loading">Loading</button>
            </div>
            <div v-else>
                <b-button class="button" @click="submit" type="is-link">
                    <span>{{ "Submit" }}</span>
                </b-button>
            </div>
        </footer>
    </div>
</template>
<script>
import bankStatementService from "@/services/bankStatementService";
import { mapMutations, mapState } from "vuex";
export default {
    data() {
        return {
            dropFiles: [],
            loading: false,
            note: "notka tymczasowa",
        };
    },
    computed: {
        ...mapState("user", ["chosenUser"]),
    },
    methods: {
        deleteDropFile(index) {
            this.dropFiles.splice(index, 1);
        },
        ...mapMutations("user", ["setChosenUser"]),
        submit() {
            if (this.dropFiles.length == 0) {
                this.$buefy.notification.open({
                    duration: 3000,
                    message: "Not found files to send!",
                    type: "is-danger",
                    hasIcon: true,
                });
            }
            for (var i = 0; i < this.dropFiles.length; i++) {
                this.loading = true;
                let formData = new FormData();
                formData.append("file", this.dropFiles[i]);
                formData.append("user", this.chosenUser.username);
                formData.append("note", this.note);
                bankStatementService
                    .uploadData(formData)
                    .then(() => {
                        this.$buefy.notification.open({
                            duration: 3000,
                            message: "Statement was sent.",
                            type: "is-success",
                            hasIcon: true,
                        });
                    })
                    .catch((err) => {
                        console.log(err);
                    })
                    .finally(() => {
                        this.deleteDropFile(0);
                        if (this.dropFiles.length == 0) {
                            this.loading = false;
                        }
                    });
            }
        },
    },
};
</script>

<style>
.modal-card-body {
    vertical-align: middle;
    text-align: center;
}
</style>
