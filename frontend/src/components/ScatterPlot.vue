<script>
import { Scatter } from "vue-chartjs";

export default {
  extends: Scatter,
  name: "ScatterPlot",
  props:{
      chartData: {
        type: Object,
        default: null
      },
      options: {
        type: Object,
        default: null,
      }
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>