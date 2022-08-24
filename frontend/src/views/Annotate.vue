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

      <DeleteModal :title="'Leaving project ' + annotationTask.project_name"
                   v-model="showLeaveProjectModal"
                   operation-string="Leave project"
                   @delete="leaveProjectHandler">
        Are you sure you want to leave this project?

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
            <h2 :class="getAnnotationSectionHeaderClass()">
              Annotate a document
            </h2>

            <b-badge v-if="annotationTask.document_type !== 'Annotation'"
                     class="ml-2 " variant="dark" pill style="font-size: 1.2em">
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
              To familiarise you with the annotation process of this project, you will be annotating some
              example documents. Expected annotation results for each label will be provided.
            </p>
          </div>
          <div v-else-if="annotationTask.document_type === 'Test'">
            <h3>Starting test stage</h3>
            <p>
              In this stage, you will be tested to ensure that you can annotate documents in accordance with
              the annotation guideline.
            </p>
          </div>
          <div v-else>
            <h3>Starting annotation</h3>
            <p>
              You're about to start annotating documents. Please make sure you've read the annotator guideline
              to make sure you know what's expected from your annotations.
            </p>
          </div>
          <b-button variant="primary" @click="showStageIntroCard = false">Start annotating</b-button>
        </b-card>
        <b-card v-else>
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
    <div class="mt-4" v-else-if="showThankyouCard">
      <h1>Thank you for participating!</h1>
      <b-card>
        <p>
          Thank you, all of your annotation tasks for the project have been completed!
        </p>
        <p>
          It's now possible to participate in annotating for other projects. Inform a project manager of your
          username if you wish to do so.
        </p>
      </b-card>
    </div>
    <div class="mt-4" v-else>
      <h1>Nothing to annotate!</h1>
      <b-card>
        <p>
          Thank you for participating. Notify the project manger of your username in order to be added to an
          annotation project.
        </p>
      </b-card>
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
      currentTaskIndex: 0,
      annotationTask: null,
      DocumentType,
      showLeaveProjectModal: false,
      showStageIntroCard: false,
      showThankyouCard: false,
    }
  },
  computed: {
    currentAnnotationTask(){
      if( "task_history" in this.annotationTask){

      }
      else{
        return this.annotationTask
      }
    }
  },
  methods: {
    ...mapActions(["getUserAnnotationTask", "completeUserAnnotationTask", "rejectUserAnnotationTask", "annotatorLeaveProject"]),
    getAnnotationContainerBgClass() {
      return {
        "mt-4": true,
        "p-2": true,
        trainingAnnotateBg: this.annotationTask.document_type === "Training",
        testAnnotateBg: this.annotationTask.document_type === "Test",
        annotateBg: this.annotationTask.document_type === "Annotation",
      }

    },
    getAnnotationSectionHeaderClass() {
      return {
        lightHeader: this.annotationTask.document_type === "Training" || this.annotationTask.document_type === "Test",
        darkHeader: this.annotationTask.document_type === "Annotation"
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

        const previousTask = this.annotationTask

        this.annotationTask = await this.getUserAnnotationTask()

        // Check that the user has not completed any task in this stage,
        // show intro card
        if (this.annotationTask) {
          if (this.annotationTask.annotation_id) {
            if (this.annotationTask.document_type === "Training" &&
                this.annotationTask.annotator_completed_training_tasks < 1) {
              this.showStageIntroCard = true
            }

            if (this.annotationTask.document_type === "Test" &&
                this.annotationTask.annotator_completed_test_tasks < 1) {
              this.showStageIntroCard = true
            }

            if (this.annotationTask.document_type === "Annotation" &&
                this.annotationTask.annotator_completed_tasks < 1) {
              this.showStageIntroCard = true
            }
          }
        }

        // Show a thankyou message if we've just completed all annotation tasks
        if (previousTask && !this.annotationTask) {
          this.showThankyouCard = true
        }

      } catch (e) {
        console.log("Still showing error for some reason")
        toastError("Could not get annotation task", e, this)
      }
    },
    async leaveProjectHandler() {
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

.lightHeader {
  color: white;
  display: inline-block;
}

.darkHeader {
  color: black;
  display: inline-block;
}


.annotateBg {
  background-image: none;
  background: white;

}

</style>
