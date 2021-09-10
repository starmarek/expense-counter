import api from "@/services/api";

export default {
    uploadData(formData) {
        return api.post(`bank_statement/loader/`, formData, { timeout: 0 });
    },
    fetchBankStatement(dataToFetch) {
        return api
            .get(`bank_statement/`, { params: dataToFetch })
            .then((response) => response.data);
    },
    deleteStatement(id) {
        return api.delete(`bank_statement/${id}`);
    },
    getPdfStatement(id) {
        return api
            .get(`bank_statement/store/`, {
                params: { ID: id },
                responseType: "arraybuffer",
            })
            .then((response) => response.data);
    },
};
