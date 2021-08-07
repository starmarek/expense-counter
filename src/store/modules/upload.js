import uploadService from "../../services/uploadService";

const state = {
    currentData: {},
};

const getters = {};

const actions = {
    onSubmit({ commit }, Data) {
        return new Promise((resolve, reject) => {
            uploadService
                .uploadData(Data)
                .then((data) => {
                    commit("setCurrentData", data);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setCurrentData(state, data) {
        state.currentData = data;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
