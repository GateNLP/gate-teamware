<template>
  <div class="container">
    <div v-if="annotationTask">
      <h1>Annotating: {{annotationTask.project_name}}</h1>
      <p>{{annotationTask.project_description}}</p>

      <AnnotationRenderer :config="annotationTask.project_config"
                          :document="annotationTask.document_data"
                          @submit="submitHandler"
                          @reject="rejectHandler"
      ></AnnotationRenderer>
    </div>
    <div v-else>
      <h1>Nothing to annotate!</h1>
      <p>
        Thank you for participating. Notify the project manger of your username in order to be added to an
        annotation project.
      </p>


    </div>

  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import AnnotationRenderer from "@/components/AnnotationRenderer";

export default {
  name: "Annotate",
  components: {AnnotationRenderer},
  data() {
    return {
      annotationTask: null
    }
  },
  computed: {


  },
  methods: {
    ...mapActions(["getUserAnnotationTask", "completeUserAnnotationTask", "rejectUserAnnotationTask"]),
    async submitHandler(value){
      try{
        this.completeUserAnnotationTask({
          annotationID: this.annotationTask.annotation_id,
          data: value
        })
        console.log("Annotation completed")


      }catch (e){
        console.warn(e)
      }

      await this.getAnnotationTask()

    },
    async rejectHandler(){
      try{
        this.rejectUserAnnotationTask(this.annotationTask.annotation_id)
        console.log("Annotation completed")


      }catch (e){
        console.warn(e)
      }

    },
    async getAnnotationTask(){
      this.annotationTask = await this.getUserAnnotationTask()

    }
  },
  async mounted() {
    await this.getAnnotationTask()
  }
}
</script>

<style scoped>

</style>
