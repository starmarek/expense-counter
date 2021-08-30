<!-- TODO -->
<!-- 3. Preprocessing data to prepare it to be plotted -->
<!-- 4. Drawing plots and embedding them into tiles -->
<!-- 5. Implementing other charts and calculating shit embedded numerically -->
<!-- 6. Fixing plots sizing (;-;)-->
<template>
    <div class="tile is-ancestor m-5 background">
        <div class="tile is-4 is-vertical is-parent">
            <div class="tile is-child box">
                <b-field label="All bank statements">
                    <b-select
                        v-model="bankstatementselect"
                        placeholder="Select bank statement..."
                        @input="onSelectInputChange"
                    >
                        <option :value="null"></option>
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
            <div class="tile is-child box">
                Wszystkie wpływy i wydatki i finalny balans i total i lokalne
            </div>
            <div class="tile is-child box">Średnie miesięczne</div>
            <div class="tile is-child box">Tutaj będą jakieś chuje</div>
        </div>
        <div class="tile is-vertical is-parent">
            <div class="tile is-child box">
                <b-carousel
                    v-model="carousel1"
                    :animated="animated"
                    :autoplay="true"
                    :pause-hover="pause"
                    :interval="3000"
                    :repeat="true"
                    :pause-info="false"
                >
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <line-chart
                                    v-if="loadedChart2"
                                    :chartData="localbalancechartdata"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ile w danej kategorii wydatków (radar wykres)
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ile zakupów jaką metodą (doughnut wykres)
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ilość dziennych operacje w miesiącu (słupkowy)
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
                    :interval="3000"
                    :repeat="true"
                    :pause-info="false"
                >
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                <line-chart
                                    v-if="loadedChart1"
                                    :chartData="totalbalancechartdata"
                                />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ile wydatków w danej kategorii total (radar)
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ile zakupów jaką metodą total (doughnut wykres)
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Ilość operacji miesięcznych total (słupkowy)
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
import { mapActions, mapMutations, mapState } from "vuex";
export default {
    components: { LineChart },
    name: "Statistics",
    data() {
        return {
            carousel1: null,
            carousel2: null,
            bankstatementselect: null,
            animated: "slide",
            pause: true,
            loadedChart1: false,
            loadedChart2: false,
            localbalancechartdata: null,
            totalbalancechartdata: null,
        };
    },
    methods: {
        fetchAllBankStatements() {
            var fetchData = {
                ordering: "-id",
                user: this.chosenUser.id,
            };
            this.getBankStatements(fetchData).catch(() => {
                this.$buefy.notification.open({
                    duration: 5000,
                    message:
                        "Unable to load data from database, check internet connection.",
                    type: "is-danger",
                });
            });
        },
        fetchAllOperations() {
            var fetchData = {
                ordering: "date",
                user: this.chosenUser.id,
            };
            this.getCurrentOperation(fetchData)
                .then(() => {
                    this.totalbalancechartdata = this.preprocessLineChartData();
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
            var fetchData = {
                ordering: "date",
                user: this.chosenUser.id,
                bank_statement: bank_statement_id,
            };
            this.getCurrentOperation(fetchData)
                .then(() => {
                    this.localbalancechartdata = this.preprocessLineChartData();
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
                        backgroundColor: "#f87979",
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
        onSelectInputChange() {
            if (this.bankstatementselect != null) {
                this.fetchBankStatementOperations(this.bankstatementselect);
            } else {
                this.localbalancechartdata = null;
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
        this.fetchAllOperations();
    },
};
</script>

<style>
.background {
    background-color: rgb(255, 255, 255);
    width: 400%;
}
</style>
