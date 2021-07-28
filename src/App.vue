<template>
    <div>
        <div v-if="userIsChosen()" class="is-flex">
            <Sidebar />
            <router-view />
        </div>
        <UserSelect v-else />
    </div>
</template>
<script>
import Sidebar from "@/components/Sidebar";
import UserSelect from "@/views/UserSelect";

export default {
    name: "Home",
    components: { Sidebar, UserSelect },
    methods: {
        userIsChosen() {
            return Object.keys(this.$store.state.user.chosenUser).length !== 0;
        },
    },
};
</script>
