import api from "@/services/api";

export default {
    fetchUsers() {
        return api.get(`user/`).then((response) => response.data);
    },
    addUser(data) {
        return api.post(`user/`, data).then((response) => response.data);
    },
};
