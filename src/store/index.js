import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import upload from "./modules/upload";
import operation from "./modules/operation";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: { user, upload, operation },
});
