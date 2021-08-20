import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Buefy from "buefy";
import ValidatedBInput from "./components/validation/ValidatedBInput";
import ValidatedBSelect from "./components/validation/ValidatedBSelect";
import "./validationRules";
import "./assets/scss/app.scss";

Vue.use(Buefy);
Vue.component("ValidatedBInput", ValidatedBInput);
Vue.component("ValidatedBSelect", ValidatedBSelect);

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount("#app");
