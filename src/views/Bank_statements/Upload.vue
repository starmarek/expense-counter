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
            <div :class="notesView">
                <div class="m-2" v-for="(file, idx) in dropFiles" :key="idx">
                    <b-field>
                        <b-input
                            class="customInput"
                            :placeholder="file.name"
                            v-model="notes[idx]"
                        ></b-input>
                    </b-field>
                </div>
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
import { mapState } from "vuex";

export default {
    data() {
        return {
            dropFiles: [],
            loading: false,
            notes: [],
            notesView: "",
            filesCounter: 0,
        };
    },
    watch: {
        dropFiles: {
            handler() {
                if (this.dropFiles.length >= 3) {
                    this.notesView = "modal-notes-many";
                } else {
                    this.notesView = "";
                }
            },
            deep: true,
        },
    },
    computed: {
        ...mapState("user", ["chosenUser"]),
    },
    methods: {
        deleteDropFile(index) {
            this.dropFiles.splice(index, 1);
            this.notes.splice(index, 1);
        },
        async submit() {
            this.filesCounter = this.dropFiles.length;
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
                    this.loading = false;
                    this.removePreviousFiles(this.dropFiles[i].name);
                    break;
                }
                if (this.dropFiles[i].name.split(".")[1] != "pdf") {
                    this.$buefy.notification.open({
                        duration: 3000,
                        message: `File ${this.dropFiles[i].name} is not pdf!`,
                        type: "is-danger",
                        hasIcon: true,
                    });
                    this.loading = false;
                    this.removePreviousFiles(this.dropFiles[i].name);
                    break;
                }
                let note = this.notes[i];
                if (typeof note === "undefined") {
                    note = "";
                }
                let formData = new FormData();
                formData.append("file", this.dropFiles[i]);
                formData.append("filename", this.dropFiles[i].name);
                formData.append("user", this.chosenUser.id);
                formData.append("note", note);
                await this.send(formData);
            }
            if (this.filesCounter == 0) {
                this.loading = false;
                this.clear();
            }
        },
        send(formData) {
            return new Promise((resolve, reject) => {
                bankStatementService
                    .uploadData(formData)
                    .then(() => {
                        this.$buefy.notification.open({
                            duration: 3000,
                            message: `Statement ${formData.get("filename")} was sent.`,
                            type: "is-success",
                            hasIcon: true,
                        });
                        this.filesCounter -= 1;
                        resolve();
                    })
                    .catch((err) => {
                        this.$buefy.notification.open({
                            duration: 3000,
                            message: err.response.data,
                            type: "is-danger",
                            hasIcon: true,
                        });
                        this.loading = false;
                        this.removePreviousFiles(
                            this.dropFiles,
                            formData.get("filename")
                        );
                        reject(err.response.data);
                    });
            });
        },
        clear() {
            while (this.dropFiles.length != 0) {
                this.deleteDropFile(0);
            }
        },
        removePreviousFiles(targetName) {
            /*
            If appears error (too large file or wrong extention), removes previous
            files from the section under drag&drop field. Takes the name of file that 
            produces an error.
            */
            let dropCopy = this.dropFiles.slice();
            for (let i = 0; dropCopy[i].name != targetName; i++) {
                this.deleteDropFile(0);
            }
        },
    },
};
</script>

<style scoped>
.customInput >>> .input[type="text"],
textarea {
    background-color: #f1efef;
}
</style>

<style>
.modal-card-body {
    vertical-align: middle;
    text-align: center;
}
.modal-notes-many {
    height: 100px;
    overflow: scroll;
}
</style>
