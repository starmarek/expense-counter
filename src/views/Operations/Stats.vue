<!-- TODO -->
<!-- 5. Calculating things embedded numerically -->
<!-- 6. Fixing plots sizing -->
<template>
    <div class="tile is-ancestor m-5 background">
        <div class="tile is-4 is-vertical is-parent">
            <div class="tile is-child box has-text-centered">
                <div class="container">
                    <h1 class="title is-6">All bank statements</h1>
                    <b-field>
                        <b-select
                            v-model="bankstatementselect"
                            @input="onSelectInputChange"
                        >
                            <option
                                v-for="statement in bankStatementData"
                                :value="statement.id"
                                :key="statement.id"
                            >
                                {{ statement.date }}
                            </option>
                        </b-select>
                    </b-field>
                </div>
            </div>
            <div class="tile is-child box has-text-centered">
                <div class="container">
                    <div class="has-background-primary-light">
                        Starting balance: <br />
                        {{ startingbalance }}
                    </div>
                    <div class="has-background-danger-light">
                        Final balance: <br />
                        {{ finalbalance }}
                    </div>
                    <div class="has-background-primary-dark has-text-primary-light">
                        Total income: <br />
                        {{ income }}
                    </div>
                    <div class="has-background-danger-dark has-text-primary-light">
                        All expenses: <br />
                        {{ expenses }}
                    </div>
                </div>
            </div>
            <div class="tile is-child box"></div>
            <div class="tile is-child box"></div>
        </div>
        <div class="tile is-vertical is-parent">
            <div class="tile is-child box">
                <b-carousel
                    v-model="carousel1"
                    :animated="animated"
                    :autoplay="true"
                    :pause-hover="pause"
                    :interval="8000"
                    :repeat="true"
                    :pause-info="false"
                    :indicator="indicator"
                    :indicator-inside="indicatorInside"
                    :indicator-style="indicatorStyle"
                >
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">Balance changes in one month</h1>
                                <line-chart
                                    v-if="loadedChart2"
                                    :chartData="localbalancechartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">
                                    Expenses by category in one month
                                </h1>
                                <polar-area-chart
                                    v-if="loadedChart2"
                                    :chartData="localcategorieschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">
                                    Expenses by operation type in one month
                                </h1>
                                <doughnut-chart
                                    v-if="loadedChart2"
                                    :chartData="localtypeschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">
                                    Daily operations in one month
                                </h1>
                                <bar-chart
                                    v-if="loadedChart2"
                                    :chartData="localoperationschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                </b-carousel>
            </div>
            <div class="tile is-child box">
                <b-carousel
                    v-model="carousel2"
                    :autoplay="true"
                    :animated="animated"
                    :pause-hover="pause"
                    :interval="8000"
                    :repeat="true"
                    :pause-info="false"
                    :indicator="indicator"
                    :indicator-inside="indicatorInside"
                    :indicator-style="indicatorStyle"
                >
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">Balance changes in total</h1>
                                <line-chart
                                    v-if="loadedChart1"
                                    :chartData="totalbalancechartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">
                                    Expenses by category in total
                                </h1>
                                <polar-area-chart
                                    v-if="loadedChart1"
                                    :chartData="totalcategorieschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">
                                    Expenses by operation type in total
                                </h1>
                                <doughnut-chart
                                    v-if="loadedChart1"
                                    :chartData="totaltypeschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <h1 class="title is-5">Daily operations in total</h1>
                                <bar-chart
                                    v-if="loadedChart1"
                                    :chartData="totaloperationschartdata"
                                    :height="200"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                </b-carousel>
            </div>
        </div>
    </div>
</template>

<script>
import LineChart from "./Charts/LineChart.vue";
import BarChart from "./Charts/BarChart.vue";
import DoughnutChart from "./Charts/DoughnutChart.vue";
import PolarAreaChart from "./Charts/PolarAreaChart.vue";
import { mapActions, mapMutations, mapState } from "vuex";
export default {
    components: { LineChart, BarChart, DoughnutChart, PolarAreaChart },
    name: "Statistics",
    data() {
        return {
            carousel1: null,
            carousel2: null,
            indicator: true,
            indicatorBackground: true,
            indicatorInside: true,
            indicatorStyle: "is-lines",
            bankstatementselect: null,
            animated: "slide",
            pause: true,
            loadedChart1: false,
            loadedChart2: false,
            localbalancechartdata: null,
            totalbalancechartdata: null,
            localoperationschartdata: null,
            totaloperationschartdata: null,
            localtypeschartdata: null,
            totaltypeschartdata: null,
            localcategorieschartdata: null,
            totalcategorieschartdata: null,
            expenses: 0,
            income: 0,
            startingbalance: 0,
            finalbalance: 0,
        };
    },
    methods: {
        fetchAllBankStatements() {
            var fetchData = {
                ordering: "-id",
                user: this.chosenUser.id,
            };
            this.getBankStatements(fetchData)
                .then(() => {
                    this.fetchAllOperations();
                    this.bankstatementselect = this.bankStatementData[0].id;
                    this.fetchBankStatementOperations(this.bankStatementData[0].id);
                })
                .catch(() => {
                    this.$buefy.notification.open({
                        duration: 5000,
                        message:
                            "Unable to load data from database, check internet connection.",
                        type: "is-danger",
                    });
                });
        },
        fetchAllOperations() {
            this.loadedChart1 = false;
            var fetchData = {
                ordering: "date",
                user: this.chosenUser.id,
            };
            this.getCurrentOperation(fetchData)
                .then(() => {
                    this.totalbalancechartdata = this.preprocessLineChartData();
                    this.totaloperationschartdata = this.preprocessBarChartData();
                    this.totaltypeschartdata = this.preprocessDoughnutChartData();
                    this.totalcategorieschartdata = this.preprocessRadarChartData();
                    this.loadedChart1 = true;
                })
                .catch(() => {
                    this.$buefy.notification.open({
                        duration: 5000,
                        message:
                            "Unable to load data from database, check internet connection.",
                        type: "is-danger",
                    });
                });
        },
        fetchBankStatementOperations(bank_statement_id) {
            this.loadedChart2 = false;
            var fetchData = {
                ordering: "date",
                user: this.chosenUser.id,
                bank_statement: bank_statement_id,
            };
            this.getCurrentOperation(fetchData)
                .then(() => {
                    this.localbalancechartdata = this.preprocessLineChartData();
                    this.localoperationschartdata = this.preprocessBarChartData();
                    this.localtypeschartdata = this.preprocessDoughnutChartData();
                    this.localcategorieschartdata = this.preprocessRadarChartData();
                    this.calculateTotalExpensesAndIncomes();
                    this.loadedChart2 = true;
                })
                .catch(() => {
                    this.$buefy.notification.open({
                        duration: 5000,
                        message:
                            "Unable to load data from database, check internet connection.",
                        type: "is-danger",
                    });
                });
        },
        preprocessLineChartData() {
            var chartData = {
                labels: [],
                datasets: [
                    {
                        label: "Balance",
                        backgroundColor: "#a10000",
                        data: [],
                    },
                ],
            };
            for (let dict in this.currentOperation) {
                chartData["labels"].push(this.currentOperation[dict].date);
                chartData["datasets"][0]["data"].push(
                    this.currentOperation[dict].balance
                );
            }
            return chartData;
        },
        preprocessBarChartData() {
            var chartData = {
                labels: [],
                datasets: [
                    {
                        label: "Daily operations",
                        backgroundColor: "#a10000",
                        data: [],
                    },
                ],
            };
            var dailyOperations = {};
            for (let dict in this.currentOperation) {
                if (this.currentOperation[dict].date in dailyOperations) {
                    dailyOperations[this.currentOperation[dict].date] += 1;
                } else {
                    dailyOperations[this.currentOperation[dict].date] = 1;
                }
            }
            for (const [key, value] of Object.entries(dailyOperations)) {
                chartData["labels"].push(key);
                chartData["datasets"][0]["data"].push(value);
            }
            return chartData;
        },
        preprocessDoughnutChartData() {
            var chartData = {
                labels: [],
                datasets: [
                    {
                        label: "Operation types",
                        backgroundColor: [
                            "#a10000",
                            "#b12700",
                            "#c03e00",
                            "#ce5400",
                            "#db6800",
                            "#e87d00",
                            "#f49100",
                            "#ffa600",
                        ],
                        data: [],
                    },
                ],
            };
            var operationTypes = {};
            for (let dict in this.currentOperation) {
                if (this.currentOperation[dict].operation_type in operationTypes) {
                    operationTypes[this.currentOperation[dict].operation_type] += 1;
                } else {
                    operationTypes[this.currentOperation[dict].operation_type] = 1;
                }
            }
            for (const [key, value] of Object.entries(operationTypes)) {
                chartData["labels"].push(key);
                chartData["datasets"][0]["data"].push(value);
            }
            return chartData;
        },
        preprocessRadarChartData() {
            var chartData = {
                labels: [],
                datasets: [
                    {
                        label: "Categories",
                        backgroundColor: [
                            "#a10000",
                            "#b12700",
                            "#c03e00",
                            "#ce5400",
                            "#db6800",
                            "#e87d00",
                            "#f49100",
                            "#ffa600",
                        ],
                        data: [],
                    },
                ],
            };
            var operationCategories = {};
            for (let dict in this.currentOperation) {
                if (this.currentOperation[dict].category in operationCategories) {
                    operationCategories[this.currentOperation[dict].category] += 1;
                } else {
                    operationCategories[this.currentOperation[dict].category] = 1;
                }
            }
            for (const [key, value] of Object.entries(operationCategories)) {
                chartData["labels"].push(key);
                chartData["datasets"][0]["data"].push(value);
            }
            return chartData;
        },
        calculateTotalExpensesAndIncomes() {
            this.income = 0;
            this.expenses = 0;
            this.startingbalance = this.currentOperation[0].balance;
            this.finalbalance =
                this.currentOperation[this.currentOperation.length - 1].balance;
            for (let dict in this.currentOperation) {
                if (parseFloat(this.currentOperation[dict].value, 10) > 0) {
                    this.income += parseFloat(this.currentOperation[dict].value, 10);
                } else {
                    this.expenses += parseFloat(this.currentOperation[dict].value, 10);
                }
            }
            this.income = this.income.toFixed(2);
            this.expenses = this.expenses.toFixed(2);
        },
        onSelectInputChange() {
            if (this.bankstatementselect != null) {
                this.fetchBankStatementOperations(this.bankstatementselect);
            } else {
                this.loadedChart1 = false;
                this.loadedChart2 = false;
                this.localbalancechartdata = null;
                this.income = 0;
                this.expenses = 0;
                this.startingbalance = 0;
                this.finalbalance = 0;
            }
        },
        ...mapActions("bank_statement", ["getBankStatements"]),
        ...mapActions("operation", ["getCurrentOperation"]),
        ...mapMutations("user", ["setChosenUser"]),
    },
    computed: {
        ...mapState("bank_statement", ["bankStatementData"]),
        ...mapState("operation", ["currentOperation", "paginationCount"]),
        ...mapState("user", ["chosenUser"]),
    },
    created() {
        this.fetchAllBankStatements();
    },
};
</script>

<style>
.background {
    background-color: rgb(255, 255, 255);
    width: 400%;
}
</style>
