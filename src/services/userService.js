import api from "@/services/api";

export default {
    fetchUser(userID) {
        return api.get(`user/${userID}`).then((response) => response.data);
    },
};
