import { extend } from "vee-validate";
import { required } from "vee-validate/dist/rules";
import validationService from "./services/validationService";

// default rules
extend("required", {
    ...required,
    message: "This field is required",
});

// custom rules
extend("backend-val", {
    validate(value, args) {
        return validationService
            .checkForDuplicate({
                app: args.app,
                model: args.model,
                field: args.field,
                value: value,
            })
            .then((data) => {
                if (data.match) return false;
                else return true;
            });
    },
    params: ["app", "model", "field"],
    message: "'{_value_}' already exists in the database",
});
