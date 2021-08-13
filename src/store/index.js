import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import operation from "./modules/operation";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: { user, operation },
});
