<template>
    <div>
        <h2 class="mt-2 mb-2">Annotation Statistics</h2>
        <h3 class="mt-2 mb-2">Completion Times</h3>
        <ScatterPlot v-if="chartDataLoaded" :chartData="chartData" :options="chartOptions" :styles="myStyles"></ScatterPlot>
        <span><b># Timed Annotations: </b>{{numTimedAnnotations}}</span><br>
        <span><b>Mean Annotation Time: </b>{{meanAnnotationTime.toFixed(2)}} seconds</span><br>
        <span><b>Median Annotation Time: </b>{{medianAnnotationTime.toFixed(2)}} seconds</span><br>
    </div>
</template>

<script>
import {mapActions} from "vuex";
import ScatterPlot from "@/components/ScatterPlot";

export default {
    name: "AnnotationStatistics",
    components:{ScatterPlot},
    data(){
        return {
            jitterOn: true,
            chartData: {},
            chartDataLoaded: false,
            height: 200,
            meanAnnotationTime: 0,
            numTimedAnnotations: 0,
            medianAnnotationTime: 0,
            chartOptions: {
                scales:{
                    xAxes: [{
                        scaleLabel:{
                            labelString: 'Time to complete annotation (seconds)',
                            display: true,
                            fontSize: 20,
                        },
                    }],
                    yAxes: [{
                        display: false,
                    }],
                },
                responsive: true,
                maintainAspectRatio: false,
            },
        }
    },
    props: {
        projectId: {
        type: String,
        default: null,
        },
    },
    methods: {
        ...mapActions(["getAnnotationTimings"]),
        async getChartData() {
            this.chartDataLoaded = false;
            let data = await this.getAnnotationTimings(this.projectId);

            if (this.jitterOn == true){
                data = this.jitter(data);
            }

            this.chartData =  {
                datasets: [{
                    label: "Annotation Completion Times",
                    data: data,
                    backgroundColor: "#005cbf",
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    pointHitRadius: 8, 
                    tooltips: {
                        enabled: false,
                    }
                }],
            }

            this.chartDataLoaded = true;

            this.calculateStatistics();

        },
        calculateStatistics(){
            let data = this.chartData.datasets[0].data;
            let arr = [];
            let sum = 0;
            let count = 0;
            for (const element of data) {
                // build an array of values
                arr.push(element.x);
                sum = sum + element.x;
                count++;
            }
            this.meanAnnotationTime = sum/count;
            this.numTimedAnnotations = count;

            // calculate the median
            arr = Float64Array.from(arr);
            arr.sort();
            if (arr.length % 2 === 0) {
                this.medianAnnotationTime = (arr[arr.length / 2 - 1] + arr[arr.length / 2]) / 2;
            }else{
                this.medianAnnotationTime = arr[(arr.length - 1) / 2];
            }
            

        },
        jitter(data) {
            return data.map(function(e) {
            var yJitter = Math.random() * (-1 - 1) + 1;
            
            return {
                x: e.x,
                y: e.y + yJitter,
                }
            });
        },
    },
    computed: {
        myStyles () {
        return {
            height: `${this.height}px`,
            position: 'relative'
        }
        }
    },
    async mounted(){
        this.getChartData();
    },
}
</script>

<style scoped>
</style>