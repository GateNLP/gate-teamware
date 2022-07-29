<template>
  <div>
    <div class="mb-2">
                <span @click="toggleAnnotationSelect" style="cursor: pointer" class="mr-1">
                  <b-badge v-if="annotation.completed" variant="success"
                           :class="{ 'docBgSelected': selected} " title="Annotation completed">
                    <b-icon-pencil-fill
                        :class="{ 'docIcon': true, 'docIconSelected': selected}"></b-icon-pencil-fill>
                  </b-badge>
                  <b-badge v-else-if="annotation.rejected" variant="danger"
                           :class="{ 'docBgSelected': selected} " title="Annotation rejected">
                    <b-icon-x-square-fill
                        :class="{ 'docIcon': true, 'docIconSelected': selected}"></b-icon-x-square-fill>
                  </b-badge>
                  <b-badge v-else-if="annotation.timed_out" variant="warning"
                           :class="{ 'docBgSelected': selected} " title="Annotation timed out">
                    <b-icon-clock
                        :class="{ 'docIcon': true, 'docIconSelected': selected}"></b-icon-clock>
                  </b-badge>
                  <b-badge v-else-if="annotation.aborted" variant="secondary"
                           :class="{ 'docBgSelected': selected} " title="Annotation aborted">
                    <b-icon-stop-fill
                        :class="{ 'docIcon': true, 'docIconSelected': selected}"></b-icon-stop-fill>
                  </b-badge>
                  <b-badge v-else variant="primary" :class="{ 'docBgSelected': selected} "
                           title="Annotation still pending">
                    <b-icon-play-fill
                        :class="{ 'docIcon': true, 'docIconSelected': selected}"></b-icon-play-fill>
                  </b-badge>
                </span>
      <strong title="ID of the annotation object. Used internally by the application.">{{ annotation.id }}</strong>
    </div>
    <div title="Annotated by">
      <b-icon-person-fill></b-icon-person-fill>
      {{ annotation.annotated_by }}
    </div>

    <div>
      <b-icon-clock></b-icon-clock>
      Created: {{ annotation.created | datetime }}
    </div>
    <div v-if="annotation.completed">
      <b-icon-clock></b-icon-clock>
      Completed: {{ annotation.completed | datetime }}
    </div>
    <div v-else-if="annotation.rejected">
      <b-icon-clock></b-icon-clock>
      Rejected: {{ annotation.rejected | datetime }}
    </div>
    <div v-else-if="annotation.timed_out">
      <b-icon-clock></b-icon-clock>
      Time out: {{ annotation.timed_out | datetime }}
    </div>
    <div v-else-if="annotation.aborted">
      <b-icon-clock></b-icon-clock>
      Aborted at: {{ annotation.aborted | datetime }}
    </div>
    <div v-else>
      <b-icon-clock></b-icon-clock>
      Will time out at: {{ annotation.times_out_at | datetime }}
    </div>

    <div class="mt-2" v-if="allowAnnotationEdit && editingAnnotation">
      <!-- Annotation editing -->
      <b-card>
        <AnnotationRenderer :config="projectConfig"
                          :document="document.data"
                          :allow_cancel="true"
                          @submit="annotationChangeSubmitHandler"
                          @cancel="editingAnnotation = false"
      >
      </AnnotationRenderer>

      </b-card>

    </div>
    <div v-else>
      <!-- Annotation display -->
      <div v-if="annotation.completed && annotation.change_list.length > 0">
        <div v-if="showHistory">
          <div v-for="change in annotation.change_list" class="mt-2 mb-2 p-2 data-bg">
            <vue-json-pretty :data="change.data"></vue-json-pretty>
            <b-row>
              <b-col title="Changed by">
                <b-icon-person-fill></b-icon-person-fill>
                {{ change.changed_by }}
              </b-col>
              <b-col title="Changed at">
                <b-icon-clock></b-icon-clock>
                {{ change.time | datetime }}
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-button @click="deleteAnnotationChangeHistoryHandler(change.id)">Delete change</b-button>
              </b-col>
            </b-row>
          </div>

        </div>
        <div v-else class="mt-2 mb-2 p-2 data-bg">
          <!-- Shows the last item-->
          <vue-json-pretty :data="annotation.change_list[annotation.change_list.length - 1].data"></vue-json-pretty>
        </div>
        <div v-if="annotation.change_list.length > 1" class="text-right">
          <a href="#" @click.prevent="showHistory = false" v-if="showHistory">Hide change history
            <b-icon-chevron-contract></b-icon-chevron-contract>
          </a>
          <a href="#" @click.prevent="showHistory = true" v-else>Show change history
            <b-icon-chevron-expand></b-icon-chevron-expand>
          </a>
        </div>
      </div>
      <div class="mt-2">
        <b-button variant="primary" @click="editingAnnotation = true">Change annotation</b-button>
      </div>

    </div>


  </div>


</template>

<script>
import AnnotationRenderer from "@/components/AnnotationRenderer";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import {mapActions} from "vuex";
import {toastError} from "@/utils";

/**
 * Shows an individual Annotation item and its change history
 *
 * Events
 * annotation-changed(annotationId) - Triggered when the annotation has changed (re-annotation)
 * selection-changed(annotation, document) - Triggered when the user presses on the toggle icon on the top left
 */
export default {
  name: "AnnotationItem",
  components: {AnnotationRenderer, VueJsonPretty},
  data() {
    return {
      showHistory: false,
      editingAnnotation: false,
    }
  },
  props: {
    annotation: {
      default: null
    },
    document: {
      default: null
    },
    projectConfig: {
      default: null,
    },
    allowAnnotationEdit: {
      default: false,
    },
    selected: {
      default: false,
    }
  },
  methods: {
    ...mapActions(["changeAnnotation", "deleteAnnotationChangeHistory"]),
    toggleAnnotationSelect() {
      this.$emit("selection-changed", this.annotation, this.document)
    },
    async deleteAnnotationChangeHistoryHandler(id){
      try{
        await this.deleteAnnotationChangeHistory(id)
        this.$emit("annotation-changed", this.annotation.id)

      } catch (e) {
        toastError("Could not reload annotation", e, this)
      }


    },
    async annotationChangeSubmitHandler(newAnnotation, elapsedTime) {
      try{
        await this.changeAnnotation({annotationID: this.annotation.id, newData: newAnnotation})
        this.$emit("annotation-changed", this.annotation.id)

      } catch (e) {
        toastError("Could not reload annotation", e, this)
      } finally {
        this.editingAnnotation = false
      }
    }
  }
}
</script>

<style scoped>

</style>
