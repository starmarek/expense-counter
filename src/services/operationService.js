import api from "@/services/api";

export default {
    fetchOperation(dataToFetch) {
        return api
            .get(`operations/`, { params: dataToFetch })
            .then((response) => response.data);
    },
};
