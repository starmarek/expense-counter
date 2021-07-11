import Vue from "vue";
import VueRouter from "vue-router";
import VueDemo from "@/views/VueDemo";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "home",
        component: VueDemo,
    },
];

const router = new VueRouter({
    mode: process.env.IS_ELECTRON ? "hash" : "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
