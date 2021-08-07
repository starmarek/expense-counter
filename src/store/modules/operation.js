import operationService from "../../services/operationService";

const state = {
    currentOperation: {},
    paginationCount: 1,
};

const getters = {};

const actions = {
    getCurrentOperation({ commit }, fetchData) {
        return new Promise((resolve, reject) => {
            operationService
                .fetchOperation(fetchData)
                .then((operation) => {
                    if (Object.prototype.hasOwnProperty.call(fetchData, "page")) {
                        commit("setPaginationCount", operation["count"]);
                        commit("setCurrentOperation", operation.results);
                        resolve();
                    } else {
                        commit("setCurrentOperation", operation);
                        resolve();
                    }
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setCurrentOperation(state, operation) {
        state.currentOperation = operation;
    },
    setPaginationCount(state, count) {
        state.paginationCount = count;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
