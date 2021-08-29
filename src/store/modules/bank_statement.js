import bankStatementService from "../../services/bankStatementService";

const state = {
    bankStatementData: [],
};

const getters = {};

const actions = {
    getBankStatements({ commit }, fetchData) {
        return new Promise((resolve, reject) => {
            bankStatementService
                .fetchBankStatement(fetchData)
                .then((bank_statement) => {
                    console.log(bank_statement);
                    commit("setBankStatement", bank_statement);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setBankStatement(state, bank_statement) {
        state.bankStatementData = bank_statement;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
