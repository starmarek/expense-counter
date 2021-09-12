import api from "@/services/api";

export default {
    fetchOperation(dataToFetch) {
        return api
            .get(`operations/`, { params: dataToFetch })
            .then((response) => response.data);
    },
    insertCategory(name) {
        return api.post(`category/`, name);
    },
    // updateCategory(name) {
    //     return api.post(`category/`, { name });
    // },
    fetchCategories() {
        return api.get(`category/`).then((response) => response.data);
    },
};
