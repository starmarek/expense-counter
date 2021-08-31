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
            <div class="m-2" v-for="(file, idx) in dropFiles" :key="idx">
                <b-field>
                    <b-input :placeholder="file.name" v-model="notes[idx]"></b-input>
                </b-field>
            </div>
        </section>
        <footer class="modal-card-foot">
            <b-button label="Close" @click="$parent.close()" />
            <b-button label="Clear" @click="clear" />
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
            notes: [],
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
                if (this.dropFiles[i].size > 1024 * 1024) {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: `File ${this.dropFiles[i].name} is too big (>1MB)`,
                        type: "is-danger",
                        hasIcon: true,
                    });
                    this.notes.shift();
                    this.loading = false;
                    break;
                }
                if (this.dropFiles[i].name.split(".")[1] != "pdf") {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: `File ${this.dropFiles[i].name} is not pdf!`,
                        type: "is-danger",
                        hasIcon: true,
                    });
                    this.notes.shift();
                    this.loading = false;
                    break;
                }
                let note = this.notes.shift();
                if (note === undefined) {
                    note = "";
                }
                let formData = new FormData();
                formData.append("file", this.dropFiles[i]);
                formData.append("filename", this.dropFiles[i].name);
                formData.append("user", this.chosenUser.username);
                formData.append("note", note);
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
                        this.$buefy.notification.open({
                            duration: 3000,
                            message: err,
                            type: "is-danger",
                            hasIcon: true,
                        });
                    })
                    .finally(() => {
                        this.deleteDropFile(0);
                        if (this.dropFiles.length == 0) {
                            this.loading = false;
                        }
                    });
            }
        },
        clear() {
            while (this.dropFiles.length != 0) {
                this.deleteDropFile(0);
                this.notes.shift();
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
