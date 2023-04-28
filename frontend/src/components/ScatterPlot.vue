<template>
  <Scatter :options="options" :data="chartData"></Scatter>
</template>
<script>
import { Scatter } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement)

export default {
  name: "ScatterPlot",
  components: { Scatter },
  props:{
      chartData: {
        type: Object,
        default: {}
      },
      options: {
        type: Object,
        default: {},
      }
  },
};
</script>
