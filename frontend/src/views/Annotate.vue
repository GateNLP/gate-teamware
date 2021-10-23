<template>
  <div class="container">
    <div v-if="annotationTask">
      <h1>Annotate</h1>
      <b-card class="mb-4">
        <h2>Current project: {{ annotationTask.project_name }}</h2>
        <p>{{ annotationTask.project_description }}</p>
      </b-card>

      <b-card class="mt-4">
        <h4 class="mb-4">Annotating document ID{{annotationTask.document_id}}</h4>

        <AnnotationRenderer :config="annotationTask.project_config"
                          :document="annotationTask.document_data"
                          @submit="submitHandler"
                          @reject="rejectHandler"
      ></AnnotationRenderer>

      </b-card>



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
  title: "Annotate",
  components: {AnnotationRenderer},
  data() {
    return {
      annotationTask: null
    }
  },
  computed: {},
  methods: {
    ...mapActions(["getUserAnnotationTask", "completeUserAnnotationTask", "rejectUserAnnotationTask"]),
    async submitHandler(value) {
      try {
        await this.completeUserAnnotationTask({
          annotationID: this.annotationTask.annotation_id,
          data: value
        })

      } catch (e) {
        console.warn(e)
      }

      await this.getAnnotationTask()

    },
    async rejectHandler() {
      try {
        await this.rejectUserAnnotationTask(this.annotationTask.annotation_id)


      } catch (e) {
        console.warn(e)
      }

      await this.getAnnotationTask()

    },
    async getAnnotationTask() {
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
