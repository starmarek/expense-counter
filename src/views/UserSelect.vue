<template>
    <div>
        <b-button
            rounded
            class="m-5 add-button"
            size="is-medium"
            icon-left="plus"
            @click="isUserAddModalActive = true"
            >New user</b-button
        >
        <b-modal
            v-model="isUserAddModalActive"
            :can-cancel="['escape', 'outside']"
            has-modal-card
            trap-focus
        >
            <UserAddModal />
        </b-modal>
        <div
            style="height: 100vh; background-color: lightgrey"
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
                <b-button size="is-medium" @click="chooseUser(user)">Choose</b-button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import UserAddModal from "@/components/user/UserAddModal";
export default {
    name: "UserSelect",
    components: { UserAddModal },
    data() {
        return {
            isUserAddModalActive: false,
        };
    },
    methods: {
        ...mapMutations("user", ["setChosenUser"]),
        chooseUser(user) {
            this.setChosenUser(user);
            if (this.$router.currentRoute.fullPath !== "/") {
                this.$router.push("/");
            }
        },
    },
    computed: {
        ...mapState("user", ["users"]),
    },
    created() {
        this.$store.dispatch("user/fetchUsers");
    },
};
</script>
<style scoped lang="scss">
.add-button {
    position: fixed;
    bottom: 0;
    color: white;
    background-color: $secondary;
}
.add-button:hover {
    color: white;
    background-color: #354fc5;
}
</style>
