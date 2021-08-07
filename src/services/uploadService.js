import api from "@/services/api";

export default {
    uploadData(formData) {
        return api
            .post(`bank_statement/loader/`, formData)
            .then((response) => response.data);
    },
};
