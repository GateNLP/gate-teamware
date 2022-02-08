<script>
import { Scatter, mixins } from "vue-chartjs";
const {reactiveProp} = mixins;

export default {
  extends: Scatter,
  name: "ScatterPlot",
  mixins: [reactiveProp],
  props:{
      chartData: {
        type: Object,
        default: null
      },
      options: {
        legend: {
          display: false,
        },
        responsive: true,
        maintainAspectRatio: false,
      },
  },
  async mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>

<style scoped>
</style>