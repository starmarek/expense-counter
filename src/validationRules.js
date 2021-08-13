import { extend } from "vee-validate";
import * as rules from "vee-validate/dist/rules";

// install all default validation rules
Object.keys(rules).forEach((rule) => {
    extend(rule, rules[rule]);
});
