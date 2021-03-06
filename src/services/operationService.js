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
    updateCategory(categoryName, operationId) {
        return api
            .patch(`operations/${operationId}/`, { category: categoryName })
            .then((response) => response.data)
            .catch((err) => err.data);
    },
    fetchCategories() {
        return api.get(`category/`).then((response) => response.data);
    },
};
