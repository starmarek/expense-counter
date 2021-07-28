<template>
    <div
        style="height: 100vh; background-color: LightGray"
        class="is-flex is-align-items-center is-justify-content-space-evenly"
    >
        <div
            class="is-flex is-flex-direction-column is-align-items-center"
            v-for="user in users"
            :key="user.id"
        >
            <figure class="image is-128x128">
                <img class="is-rounded" src="@/assets/user_logo.png" />
            </figure>
            <p style="color: black" class="title">
                {{ user.first_name }} {{ user.last_name }}
            </p>
            <b-button @click="setChosenUser(user)">Choose</b-button>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
    name: "UserSelect",
    methods: {
        ...mapMutations("user", ["setChosenUser"]),
    },
    computed: {
        ...mapState("user", ["users"]),
    },
    created() {
        this.$store.dispatch("user/fetchUsers");
    },
};
</script>
