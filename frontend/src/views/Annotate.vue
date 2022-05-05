<template>
  <b-container>
    <div v-if="annotationTask">
      <h1>Annotate: {{ annotationTask.project_name }}</h1>


      <b-card class="mb-4">
        <div v-if="annotationTask.project_description && annotationTask.project_description.length > 0">
          <h3>Project description</h3>
          <MarkdownRenderer :content="annotationTask.project_description"></MarkdownRenderer>
        </div>

        <div v-if="annotationTask.project_annotator_guideline && annotationTask.project_annotator_guideline.length > 0">
          <h3>Annotator guideline</h3>
          <CollapseText>
            <MarkdownRenderer :content="annotationTask.project_annotator_guideline"></MarkdownRenderer>
          </CollapseText>
        </div>


      </b-card>

      <b-row class="mt-4">
        <b-col>
          <h2>
            Annotate a document
          </h2>
        </b-col>
        <b-col class="text-right">
          <b-badge :title="'Current annotating document ID: '+annotationTask.document_field_id" class="mr-2">
            #{{ annotationTask.document_field_id }}
          </b-badge>
          <b-badge variant="success"
                   :title="`You have completed ${annotationTask.annotator_completed_tasks} annotation task(s) in this project.`"
                   class="mr-2">
            <b-icon-check-square-fill></b-icon-check-square-fill>
            {{ annotationTask.annotator_completed_tasks }}
          </b-badge>
          <b-badge variant="warning"
                   :title="`You have ${annotationTask.annotator_remaining_tasks} remaining annotation task(s) in this project.`">
            <b-icon-pencil-fill></b-icon-pencil-fill>
            {{ annotationTask.annotator_remaining_tasks }}
          </b-badge>
        </b-col>
      </b-row>
      <b-card class="mb-4">


        <AnnotationRenderer :config="annotationTask.project_config"
                            :document="annotationTask.document_data"
                            :document_type="annotationTask.document_type"
                            :doc_gold_field="annotationTask.document_gold_standard_field"
                            :allow_document_reject="annotationTask.allow_document_reject"
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

  </b-container>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import MarkdownRenderer from "@/components/MarkdownRenderer";
import CollapseText from "@/components/CollapseText";
import {toastError} from "@/utils";

export default {
  name: "Annotate",
  title: "Annotate",
  components: {CollapseText, MarkdownRenderer, AnnotationRenderer},
  data() {
    return {
      annotationTask: null
    }
  },
  computed: {},
  methods: {
    ...mapActions(["getUserAnnotationTask", "completeUserAnnotationTask", "rejectUserAnnotationTask"]),
    async submitHandler(value, time) {
      try {
        await this.completeUserAnnotationTask({
          annotationID: this.annotationTask.annotation_id,
          data: value,
          annotationTime: time,
        })

      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }

      await this.getAnnotationTask()

    },
    async rejectHandler() {
      try {
        await this.rejectUserAnnotationTask(this.annotationTask.annotation_id)
      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }

      await this.getAnnotationTask()

    },
    async getAnnotationTask() {
      try {
        this.annotationTask = await this.getUserAnnotationTask()

      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }
    }
  },
  async mounted() {
    await this.getAnnotationTask()
  }
}
</script>

<style scoped>

</style>
