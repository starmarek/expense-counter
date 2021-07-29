<template>
    <b-sidebar position="static" fullheight open style="height: 100vh">
        <div class="p-1">
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
        </div>
    </b-sidebar>
</template>
<script>
import { mapMutations } from "vuex";

export default {
    name: "Sidebar",
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
