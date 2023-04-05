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
        <template #header>
          <h4>Change annotation</h4>
          <p>
            Re-annotate the document using the form below.
          </p>
        </template>
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
          <!-- Shows entire history list -->
          <div v-for="change in annotation.change_list" class="mt-2 mb-2 p-2 data-bg">
            <b-row>
              <b-col title="Changed by">
                <b-icon-person-fill></b-icon-person-fill>
                {{ change.changed_by }}
              </b-col>
              <b-col title="Changed at">
                <b-icon-clock></b-icon-clock>
                {{ change.time | datetime }}
              </b-col>
              <b-col class="text-right">
                <b-button v-if="allowChangeDelete" @click="deleteAnnotationChangeHistoryHandler(change.id)"
                          size="sm" title="Delete this change history" variant="danger" squared
                          data-role="annotation-change-delete">
                  <b-icon-x></b-icon-x>
                </b-button>
              </b-col>
            </b-row>

            <DeleteModal title="Delete this annotation change?"
                         v-model="showDeleteModal"
                         :delete-locking="false"
                         @delete="confirmDeleteAnnotationChangeHistoryHandler"
            ></DeleteModal>

            <div v-if="documentDisplayFormat === 'CSV'" data-role="annotation-display-csv">
              <b-table :items="jsonToTableData(change.data)">
                <template #head()="{ column }">
                  {{ column }}
                </template>
              </b-table>
            </div>
            <div v-else data-role="annotation-display-json">
              <vue-json-pretty :data="change.data"></vue-json-pretty>
            </div>


          </div>

        </div>
        <div v-else class="mt-2 mb-2 p-2">
          <!-- Shows the last (latest) item-->
          <div v-if="documentDisplayFormat === 'CSV'" data-role="annotation-display-csv">
            <b-table :items="jsonToTableData(annotation.change_list[annotation.change_list.length - 1].data)">
              <template #head()="{ column }">
                {{ column }}
              </template>
            </b-table>
          </div>
          <div v-else class="data-bg" data-role="annotation-display-json">
            <vue-json-pretty :data="annotation.change_list[annotation.change_list.length - 1].data"></vue-json-pretty>
          </div>
        </div>

        <div v-if="annotation.change_list.length > 1" class="text-right">
          <!-- Button to show/hide change history -->
          <a href="#" @click.prevent="showHistory = false" v-if="showHistory">Hide change history
            <b-icon-chevron-contract></b-icon-chevron-contract>
          </a>
          <a href="#" @click.prevent="showHistory = true" v-else>Show change history
            <b-icon-chevron-expand></b-icon-chevron-expand>
          </a>
        </div>

      </div>
      <div class="mt-2" v-if="allowAnnotationEdit">
        <b-button variant="primary" @click="editingAnnotation = true">Change annotation</b-button>
      </div>

    </div>


  </div>


</template>

<script>
import AnnotationRenderer from "@/components/AnnotationRenderer.vue";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import {mapActions} from "vuex";
import {flatten, toastError, toastSuccess} from "@/utils";
import DeleteModal from "@/components/DeleteModal.vue";

/**
 * Shows an individual Annotation item and its change history
 *
 * Events
 * annotation-changed(annotationId) - Triggered when the annotation has changed (re-annotation, or delete annotation history)
 * selection-changed(annotation, document) - Triggered when the user presses on the toggle icon on the top left
 */
export default {
  name: "AnnotationItem",
  components: {DeleteModal, AnnotationRenderer, VueJsonPretty},
  data() {
    return {
      showHistory: false,
      editingAnnotation: false,
      showDeleteModal: false,
      annotationChangeHistoryIdToDelete: null,
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
    },
    allowChangeDelete: {
      default: false,
    },
    /**
     * Between json or csv
     */
    documentDisplayFormat: {
      default: "json"
    },
  },
  methods: {
    ...mapActions(["changeAnnotation", "deleteAnnotationChangeHistory"]),
    jsonToTableData(data) {
      return [flatten(data)]
    },
    toggleAnnotationSelect() {
      this.$emit("selection-changed", this.annotation, this.document)
    },
    async deleteAnnotationChangeHistoryHandler(id) {
      this.showDeleteModal = true
      this.annotationChangeHistoryIdToDelete = id

    },
    async confirmDeleteAnnotationChangeHistoryHandler() {

      try {
        await this.deleteAnnotationChangeHistory(this.annotationChangeHistoryIdToDelete)
        this.$emit("annotation-changed", this.annotation.id)
        toastSuccess("Delete confirmed", "The annotation change has been deleted.")

      } catch (e) {
        toastError("Could not reload annotation", e, this)
      }

    },
    async annotationChangeSubmitHandler(newAnnotation, elapsedTime) {
      try {
        await this.changeAnnotation({annotationID: this.annotation.id, newData: newAnnotation})
        this.$emit("annotation-changed", this.annotation.id)
        toastSuccess("Annotation changed", "The annotation has been successfully changed.")

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
