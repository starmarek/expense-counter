import api from "@/services/api";

export default {
    fetchUsers() {
        return api.get(`user/`).then((response) => response.data);
    },
    addUser(data) {
        return api.post(`user/`, data).then((response) => response.data);
    },
    delUser(idOfUserToDel) {
        return api.delete(`user/${idOfUserToDel}/`).then((response) => response.data);
    },
};
