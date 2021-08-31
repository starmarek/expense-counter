<script>
import { Doughnut } from "vue-chartjs";
export default {
    extends: Doughnut,
    props: {
        chartData: {
            type: Object,
            default: null,
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
        },
    },
    mounted() {
        this.renderChart(this.chartData, this.options);
    },
};
</script>
