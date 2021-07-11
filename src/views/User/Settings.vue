<template>
    <div>
        <p v-for="key in Object.keys(currentUser)" :key="key">
            <strong>{{ key }}: </strong>{{ currentUser[key] }}
        </p>
    </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
    name: "Settings",
    computed: {
        ...mapState("user", ["currentUser"]),
    },
    methods: {
        ...mapActions("user", ["getCurrentUser"]),
    },
    created() {
        // below line will fail if user with ID=1 is not present in DB
        // TODO: remove ID=1 hardcode and fetch user that was chosen at the start of application
        this.getCurrentUser(1).catch(() => {
            this.$buefy.notification.open({
                duration: 5000,
                message: "Add user with ID=1 to DB, or refactor the code :)",
                type: "is-danger",
            });
        });
    },
};
</script>
