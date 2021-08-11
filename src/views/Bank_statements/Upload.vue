<template>
    <div class="containerUpload">
        <section>
            <b-field>
                <b-button class="button" @click="submit" type="is-link">
                    <span>{{ "Submit" }}</span>
                </b-button>
            </b-field>
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

            <div class="itemsBar">
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
.containerUpload {
    display: flex;
    flex-direction: row;
    /* background-color: rgb(171, 181, 185); */
    justify-content: center;
    align-items: center;
    width: 500%;
}
/* .upload {
    background-color: white;
} */
.itemsBar {
    width: 11cm;
}
.button {
    left: 40%;
}
</style>
