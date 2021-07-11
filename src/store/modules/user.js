import userService from "../../services/userService";

const state = {
    currentUser: {},
};

const getters = {};

const actions = {
    getCurrentUser({ commit }, userID) {
        return new Promise((resolve, reject) => {
            userService
                .fetchUser(userID)
                .then((user) => {
                    commit("setCurrentUser", user);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setCurrentUser(state, user) {
        state.currentUser = user;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
