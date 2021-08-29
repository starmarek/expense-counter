<template>
    <div>
        <b-field label="Name" horizontal>
            <b-input v-model="name"></b-input>
        </b-field>
        <b-button @click="deleteFile">Click Me</b-button>
        <ul v-if="isLoaded">
            <li v-for="(file, idx) in files" :key="idx">
                {{ file }}
            </li>
        </ul>
    </div>
</template>

<script>
import bankStatementService from "@/services/bankStatementService";
import { mapActions, mapState, mapMutations } from "vuex";
export default {
    data() {
        return {
            files: [],
            name: "",
            isLoaded: false,
        };
    },
    created() {
        var fetchData = { ordering: "-id", user: this.chosenUser.id };
        this.getBankStatements(fetchData)
            .then(() => {
                this.isLoaded = true;
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
    methods: {
        ...mapActions("bank_statement", ["getBankStatements"]),
        ...mapMutations("user", ["setChosenUser"]),
        loadAsyncData() {
            bankStatementService
                .getStatements()
                .then((response) => {
                    this.files = response["data"];
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        deleteFile() {
            console.log(this.name);
            bankStatementService
                .deleteStatement(this.name)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
            this.loadAsyncData();
        },
    },
};
</script>

<style></style>
