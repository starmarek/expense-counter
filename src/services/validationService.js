import api from "@/services/api";

export default {
    checkForDuplicate(params) {
        return api
            .get(`validation-view/`, {
                params: params,
            })
            .then((response) => response.data);
    },
};
