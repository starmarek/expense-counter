import Vue from "vue";
import VueRouter from "vue-router";
import Dashboard from "@/views/Dashboard";
import History from "@/views/Operations/History";
import Stats from "@/views/Operations/Stats";
import Store from "@/views/Bank_statements/Store";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "dashboard",
        component: Dashboard,
    },
    {
        path: "/operations-stats",
        name: "operations-stats",
        component: Stats,
    },
    {
        path: "/operations-history",
        name: "operations-history",
        component: History,
    },
    {
        path: "/bank_statements-store",
        name: "bank_statements-store",
        component: Store,
    },
];

const router = new VueRouter({
    mode: process.env.IS_ELECTRON ? "hash" : "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
