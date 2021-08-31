<script>
import { PolarArea } from "vue-chartjs";
export default {
    extends: PolarArea,
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
