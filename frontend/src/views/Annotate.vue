<template>
  <b-container>
    <div v-if="currentAnnotationTask">
      <b-row class="mt-4">
        <b-col cols="9">
          <h1>Annotate: {{ currentAnnotationTask.project_name }}</h1>

        </b-col>
        <b-col cols="3" class="text-right">
          <b-button variant="danger" @click="showLeaveProjectModal = true">
            Leave project
          </b-button>
        </b-col>
      </b-row>

      <DeleteModal :title="'Leaving project ' + currentAnnotationTask.project_name"
                   v-model="showLeaveProjectModal"
                   operation-string="Leave project"
                   @delete="leaveProjectHandler">
        Are you sure you want to leave this project?

      </DeleteModal>


      <b-card class="mb-4">
        <div v-if="currentAnnotationTask.project_description && currentAnnotationTask.project_description.length > 0">
          <h3>Project description</h3>
          <MarkdownRenderer :content="currentAnnotationTask.project_description"></MarkdownRenderer>
        </div>

        <div
            v-if="currentAnnotationTask.project_annotator_guideline && currentAnnotationTask.project_annotator_guideline.length > 0">
          <h3>Annotator guideline</h3>
          <CollapseText>
            <MarkdownRenderer :content="currentAnnotationTask.project_annotator_guideline"></MarkdownRenderer>
          </CollapseText>
        </div>


      </b-card>

      <div v-if="currentAnnotationTask.annotation_id" :class="getAnnotationContainerBgClass()">
        <b-row>
          <b-col cols="9">
            <h2 :class="getAnnotationSectionHeaderClass()">
              Annotate a document
            </h2>

            <b-badge v-if="currentAnnotationTask.document_type !== 'Annotation'"
                     class="ml-2 " variant="dark" pill style="font-size: 1.2em">
              {{ currentAnnotationTask.document_type }} stage
            </b-badge>

          </b-col>
          <b-col class="text-right">
            <b-badge :title="'Currently annotating document ID: '+currentAnnotationTask.document_field_id" class="mr-2">
              #{{ currentAnnotationTask.document_field_id }}
            </b-badge>
            <b-badge variant="success"
                     :title="`You have completed ${currentAnnotationTask.annotator_completed_tasks} annotation task(s) in this project.`"
                     class="mr-2">
              <b-icon-check-square-fill></b-icon-check-square-fill>
              {{ currentAnnotationTask.annotator_completed_tasks }}
            </b-badge>
            <b-badge variant="warning"
                     :title="`You have ${currentAnnotationTask.annotator_remaining_tasks} remaining annotation task(s) in this project.`">
              <b-icon-pencil-fill></b-icon-pencil-fill>
              {{ currentAnnotationTask.annotator_remaining_tasks }}
            </b-badge>
          </b-col>
        </b-row>

        <b-card class="text-center" v-if="showStageIntroCard">
          <div v-if="currentAnnotationTask.document_type === 'Training'">
            <h3>Starting training stage</h3>
            <p>
              To familiarise you with the annotation process of this project, you will be annotating some
              example documents. Expected annotation results for each label will be provided.
            </p>
          </div>
          <div v-else-if="currentAnnotationTask.document_type === 'Test'">
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
          <AnnotationRenderer ref="annotationRenderer"
                              :config="currentAnnotationTask.project_config"
                              :document="currentAnnotationTask.document_data"
                              :document_type="currentAnnotationTask.document_type"
                              :doc_gold_field="currentAnnotationTask.document_gold_standard_field"
                              :doc_preannotation_field="currentAnnotationTask.document_pre_annotation_field"
                              :allow_document_reject="isLatestTask() && currentAnnotationTask.allow_document_reject"
                              :clear_after_submit="clearFormAfterSubmit"
                              @submit="submitHandler"
                              @reject="rejectHandler"
          ></AnnotationRenderer>


        </b-card>

        <b-button-toolbar v-if="'task_history' in annotationTask" class="mt-4">
          <b-button-group>
            <b-button :disabled="!hasPreviousTask()" @click="toPreviousTask" variant="primary" size="sm"
                      title="Navigate to previous annotation task to modify your previous annotation.">
              <b-icon-chevron-bar-left></b-icon-chevron-bar-left>
              Previous task
            </b-button>
            <b-button :disabled="!hasNextTask()" @click="toNextTask" variant="primary" size="sm"
                      title="Navigate to the next annotation task.">
              Next task
              <b-icon-chevron-bar-right></b-icon-chevron-bar-right>
            </b-button>
            <b-button :disabled="isLatestTask()" @click="toLatestTask" variant="primary" size="sm"
                      title="Navigate to the current annotation task.">
              Current task
              <b-icon-chevron-double-right></b-icon-chevron-double-right>
            </b-button>
          </b-button-group>
        </b-button-toolbar>


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
import {toastError, toastSuccess} from "@/utils";
import {DocumentType} from '@/enum/DocumentTypes';
import DeleteModal from "@/components/DeleteModal";

export default {
  name: "Annotate",
  title: "Annotate",
  components: {DeleteModal, CollapseText, MarkdownRenderer, AnnotationRenderer},
  data() {
    return {
      clearFormAfterSubmit: true,
      currentTaskIndex: 0,
      annotationTask: null,
      currentAnnotationTask: null,
      DocumentType,
      showLeaveProjectModal: false,
      showStageIntroCard: false,
      showThankyouCard: false,
    }
  },

  methods: {
    ...mapActions(["getUserAnnotationTask", "getUserAnnotationTaskWithID",
      "completeUserAnnotationTask", "rejectUserAnnotationTask", "annotatorLeaveProject",
      "changeAnnotation"]),
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
    isLatestTask(){
      return this.currentTaskIndex === 0
    },
    // Checks that there is previous task in the task_history
    hasPreviousTask() {
      if ("task_history" in this.annotationTask) {
        return this.currentTaskIndex + 1 < this.annotationTask["task_history"].length
      }
      return false

    },
    // Checks that there is a next task in task_history
    hasNextTask() {
      if ("task_history" in this.annotationTask) {
        return this.currentTaskIndex > 0
      }
      return false
    },
    // Go to previous task in the history
    toPreviousTask() {
      if (this.hasPreviousTask()) {
        this.currentTaskIndex += 1
        this.getCurrentTask()
      }
    },
    // Goes to next task in history
    toNextTask() {
      if (this.hasNextTask()) {
        this.currentTaskIndex -= 1
        this.getCurrentTask()
      }
    },
    // Goes to the latest task
    toLatestTask() {
      this.currentTaskIndex = 0
      this.getCurrentTask()
    },
    async getCurrentTask() {
      try {

        if (this.annotationTask != null && "task_history" in this.annotationTask) {
          const annotationId = this.annotationTask["task_history"][this.currentTaskIndex]


          if (annotationId === this.annotationTask.id) {
            this.currentAnnotationTask = this.annotationTask
            this.clearFormAfterSubmit = true
          } else {
            this.currentAnnotationTask = await this.getUserAnnotationTaskWithID(annotationId)
            this.clearFormAfterSubmit = false
          }
        } else {
          this.currentAnnotationTask = this.annotationTask
          this.clearFormAfterSubmit = true
        }


        //Fills the annotation renderer with data
        if (this.$refs.annotationRenderer) {
          this.$refs.annotationRenderer.clearForm()
          if (this.currentAnnotationTask && this.currentAnnotationTask.annotation_data != null)
            this.$refs.annotationRenderer.setAnnotationData(this.currentAnnotationTask.annotation_data)
        }

      } catch (e) {
        toastError("Could not get annotation task", e, this)
        console.log(e)
      }
    },
    async submitHandler(value, time) {

      if (this.isLatestTask()) {
        // Complete a current task
        try {

          await this.completeUserAnnotationTask({
            annotationID: this.annotationTask.annotation_id,
            data: value,
            annotationTime: time,
          })

          await this.getAnnotationTask()
        } catch (e) {
          toastError("Could not get annotation task", e, this)
        }
      } else {
        // Change a previous annotation task
        try {
          await this.changeAnnotation({
            annotationID: this.currentAnnotationTask.annotation_id,
            newData: value
          })
          toastSuccess("Annotation changed", "Annotation for this document has been successfully changed.")
        } catch (e) {
          toastError("Could not  complete annotation task", e, this)
        }

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

    }
    ,
    async getAnnotationTask() {
      try {

        const previousTask = this.annotationTask

        this.annotationTask = await this.getUserAnnotationTask()
        this.currentTaskIndex = 0
        this.getCurrentTask()

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
    }
    ,
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
