import Vue from "vue";
import VueRouter from "vue-router";
import Dashboard from "@/views/Dashboard";
import Settings from "@/views/User/Settings";
import Upload from "@/views/Bank_statements/Upload";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "dashboard",
        component: Dashboard,
    },
    {
        path: "/user-settings",
        name: "user-settings",
        component: Settings,
    },
    {
        path: "/statement-upload",
        name: "statement-upload",
        component: Upload,
    },
];

const router = new VueRouter({
    mode: process.env.IS_ELECTRON ? "hash" : "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
