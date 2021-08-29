import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import operation from "./modules/operation";
import bank_statement from "./modules/bank_statement";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: { user, operation, bank_statement },
});
