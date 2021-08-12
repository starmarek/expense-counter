<template>
    <div class="modal-card" style="width: 400px">
        <header class="modal-card-head">
            <p class="modal-card-title">Upload your statemant as PDF</p>
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
            <b-button class="button" @click="submit" type="is-link">
                <span>{{ "Submit" }}</span>
            </b-button>
        </footer>
    </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
export default {
    computed: {
        ...mapState("upload", ["currentData"]),
    },
    data() {
        return {
            file: {},
            dropFiles: [],
        };
    },
    methods: {
        ...mapActions("upload", ["onSubmit"]),

        deleteDropFile(index) {
            this.dropFiles.splice(index, 1);
        },
        submit() {
            if (this.dropFiles.length != 0) {
                let formData = new FormData();
                for (var i = 0; i < this.dropFiles.length; i++) {
                    let file = this.dropFiles[i];
                    formData.append("file_" + (i + 1), file);
                }
                this.onSubmit(formData);
                while (this.dropFiles.length != 0) {
                    this.deleteDropFile(0);
                }
                this.$buefy.notification.open({
                    duration: 3000,
                    message: "Statement was sent.",
                    type: "is-success",
                    hasIcon: true,
                });
            } else {
                this.$buefy.notification.open({
                    duration: 3000,
                    message: "Not found files to send!",
                    type: "is-danger",
                    hasIcon: true,
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
