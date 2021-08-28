<template>
    <div class="tile is-ancestor m-5 background">
        <div class="tile is-4 is-vertical is-parent">
            <div class="tile is-child box">Tutaj będzie pole wyboru</div>
            <div class="tile is-child box">Tutaj będą jakieś dane</div>
            <div class="tile is-child box">Tutaj będą inne dane</div>
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
                            <div class="hero-body">
                                <line-chart :chartData="data1" />
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Tutaj jest wykres 2
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Tutaj jest wykres 3
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
                                Tutaj jest wykres kołowy 1
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Tutaj jest wykres kołowy 2
                            </div>
                        </section>
                    </b-carousel-item>
                    <b-carousel-item>
                        <section class="hero is-medium">
                            <div class="hero-body has-text-centered">
                                Tutaj jest wykres kołowy 3
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
export default {
    components: { LineChart },
    name: "Statistics",
    data() {
        return {
            carousel1: 0,
            carousel2: 1,
            animated: "slide",
            pause: true,
            data1: {
                labels: ["test1", "test2", "test3"],
                datasets: [
                    {
                        label: "Set 1",
                        bacgroundColor: "#f87979",
                        data: [10, 5, 12],
                    },
                ],
            },
        };
    },
    created() {
        console.log("Created");
    },
};
</script>

<style>
.background {
    background-color: rgb(255, 255, 255);
    width: 400%;
}
</style>
