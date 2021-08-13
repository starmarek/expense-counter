import api from "@/services/api";

export default {
    uploadData(formData) {
        return api.post(`bank_statement/loader/`, formData, { timeout: 0 });
    },
};
