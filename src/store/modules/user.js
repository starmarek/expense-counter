import userService from "../../services/userService";

const state = {
    users: [],
    chosenUser: {},
};

const getters = {};

const actions = {
    fetchUsers({ commit }) {
        return new Promise((resolve, reject) => {
            userService
                .fetchUsers()
                .then((users) => {
                    commit("setUsers", users);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    addUser({ commit, state }, userToAdd) {
        return new Promise((resolve, reject) => {
            userService
                .addUser(userToAdd)
                .then((user) => {
                    commit("setUsers", [...state.users, user]);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    delUser({ commit, state }, idOfUserToDel) {
        return new Promise((resolve, reject) => {
            userService
                .delUser(idOfUserToDel)
                .then(() => {
                    commit(
                        "setUsers",
                        state.users.filter((item) => item.id !== idOfUserToDel)
                    );
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setUsers(state, users) {
        state.users = users;
    },
    setChosenUser(state, user) {
        state.chosenUser = user;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
