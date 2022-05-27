<template>
  <b-container>
    <div v-if="annotationTask">
      <b-row class="mt-4">
        <b-col cols="9">
          <h1>Annotate: {{ annotationTask.project_name }}</h1>

        </b-col>
        <b-col cols="3" class="text-right">
          <b-button variant="danger" @click="showLeaveProjectModal = true">
            Leave project
          </b-button>
        </b-col>
      </b-row>

      <DeleteModal title="Leaving project"
                   v-model="showLeaveProjectModal"
                   operation-string="Leave project"
                   @delete="leaveProjectHandler">
        Some message

      </DeleteModal>



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

      <div v-if="annotationTask.annotation_id" :class="getAnnotationContainerBgClass()">
        <b-row>
          <b-col cols="9">
            <h2 style="color: white; display: inline-block">
              Annotate a document
            </h2>

            <b-badge class="ml-2 " variant="dark" pill style="font-size: 1.2em">
                  {{ annotationTask.document_type }} stage
                </b-badge>

          </b-col>
          <b-col class="text-right">
            <b-badge :title="'Currently annotating document ID: '+annotationTask.document_field_id" class="mr-2">
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

        <b-card class="text-center" v-if="showStageIntroCard">
          <div v-if="annotationTask.document_type === 'Training'">
            <h3>Starting training stage</h3>
            <p>
              Stage explanation
            </p>
          </div>
          <div v-else-if="annotationTask.document_type === 'Test'">
            <h3>Starting test stage</h3>
            <p>
              Stage explanation
            </p>
          </div>
          <div v-else>
            <h3>Starting annotation</h3>
            <p>
              Stage explanation
            </p>
          </div>
          <b-button variant="primary" @click="showStageIntroCard = false">Start annotating</b-button>
        </b-card>
        <b-card class="mt-4" v-else>
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
        <h2>Waiting for approval to perform annotation</h2>
        <b-card>
          You require approval from the project manager to proceed with the annotation task.
        </b-card>
      </div>

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
import {DocumentType} from '@/enum/DocumentTypes';
import DeleteModal from "@/components/DeleteModal";

export default {
  name: "Annotate",
  title: "Annotate",
  components: {DeleteModal, CollapseText, MarkdownRenderer, AnnotationRenderer},
  data() {
    return {
      annotationTask: null,
      DocumentType,
      showLeaveProjectModal: false,
      showStageIntroCard: false,
    }
  },
  computed: {},
  methods: {
    ...mapActions(["getUserAnnotationTask", "completeUserAnnotationTask", "rejectUserAnnotationTask", "annotatorLeaveProject"]),
    getAnnotationContainerBgClass(){
      return {
        "mt-4": true,
        "p-2": true,
        trainingAnnotateBg: this.annotationTask.document_type === "Training",
        testAnnotateBg: this.annotationTask.document_type === "Test",
        annotateBg: this.annotationTask.document_type === "Annotation",
      }

    },
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

      try {
        await this.getAnnotationTask()
      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }

    },
    async rejectHandler() {
      try {
        await this.rejectUserAnnotationTask(this.annotationTask.annotation_id)
      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }

      try {
        await this.getAnnotationTask()
      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }

    },
    async getAnnotationTask() {
      try {
        this.annotationTask = await this.getUserAnnotationTask()

        // Check that the user has not completed any task in this stage,
        // show intro card
        if(this.annotationTask.annotation_id){
          if(this.annotationTask.document_type === "Training" &&
              this.annotationTask.annotator_completed_training_tasks < 1){
            this.showStageIntroCard = true
          }

          if(this.annotationTask.document_type === "Test" &&
              this.annotationTask.annotator_completed_test_tasks < 1){
            this.showStageIntroCard = true
          }

          if(this.annotationTask.document_type === "Annotation" &&
              this.annotationTask.annotator_completed_tasks < 1){
            this.showStageIntroCard = true
          }

        }

      } catch (e) {
        toastError("Could not get annotation task", e, this)
      }
    },
    async leaveProjectHandler(){
      try {
        await this.annotatorLeaveProject()
      } catch (e) {
        toastError("Could not leave project", e, this)
      }

      try {
        await this.getAnnotationTask()
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

.trainingAnnotateBg {
  background-image: linear-gradient(#02ac53, white);

}

.testAnnotateBg {
  background-image: linear-gradient(#e56e11, white);

}



.annotateBg {
  background-image: linear-gradient(#4db1c1, white);

}

</style>
