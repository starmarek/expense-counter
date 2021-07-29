<template>
    <b-sidebar position="static" fullheight open>
        <div
            style="height: 100vh; background-color: lightGrey"
            class="
                is-flex is-flex-direction-column is-justify-content-space-between
                p-1
            "
        >
            <b-menu>
                <b-menu-list label="Menu">
                    <b-menu-item
                        @click="pushTo('/')"
                        icon="checkerboard"
                        label="Dashboard"
                    ></b-menu-item>
                    <b-menu-item icon="cash-multiple" label="Expenses">
                        <b-menu-item icon="chart-line" label="Statistics"></b-menu-item>
                        <b-menu-item icon="history" label="History"></b-menu-item>
                    </b-menu-item>
                    <b-menu-item icon="book" label="Bank statements">
                        <b-menu-item
                            @click="pushTo('/statement-upload')"
                            icon="upload"
                            label="Upload new"
                        ></b-menu-item>
                        <b-menu-item icon="history" label="History"></b-menu-item>
                    </b-menu-item>
                    <b-menu-item icon="account" label="Account">
                        <b-menu-item icon="settings" label="Settings"></b-menu-item>
                        <b-menu-item
                            @click="setChosenUser({})"
                            icon="account-switch"
                            label="Switch accounts"
                        ></b-menu-item>
                    </b-menu-item>
                </b-menu-list>
            </b-menu>
            <div>
                <hr style="margin: 0" />
                <div style="height: 100%" class="media">
                    <figure class="media-left m-2">
                        <p class="image is-64x64">
                            <img class="is-rounded" src="@/assets/user_logo.png" />
                        </p>
                    </figure>
                    <div
                        class="
                            is-flex is-justify-content-center is-align-items-center
                            media-content
                        "
                        style="height: 100%"
                    >
                        <b>{{ chosenUser.first_name }} {{ chosenUser.last_name }}</b>
                    </div>
                </div>
            </div>
        </div>
    </b-sidebar>
</template>
<script>
import { mapMutations, mapState } from "vuex";

export default {
    name: "Sidebar",
    computed: {
        ...mapState("user", ["chosenUser"]),
    },
    methods: {
        pushTo(path) {
            if (this.$router.currentRoute.fullPath !== path) {
                this.$router.push(path);
            }
        },
        ...mapMutations("user", ["setChosenUser"]),
    },
};
</script>
