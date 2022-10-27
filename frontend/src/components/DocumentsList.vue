<template>
  <b-overlay :show="isLoading">
    <b-button-toolbar v-if="showMenuBar" class="mt-2 mb-2">
      <b-button-group>
        <b-button v-if="isPageSelected()"
                  :title="'Clear selection. (' + selectedDocs.size + ' documents and ' + selectedAnnotations.size + ' annotations selected)'"
                  @click="clearDocumentSelection()">
          <b-icon-check-square></b-icon-check-square>
          <span style="width: 30px">&nbsp;</span>
          {{ selectedDocs.size }}
          <b-icon-file-earmark-text></b-icon-file-earmark-text>
          {{ selectedAnnotations.size }}
          <b-icon-pencil-square></b-icon-pencil-square>
        </b-button>
        <b-button v-else
                  :title="'Select all (' + selectedDocs.size + ' documents and ' + selectedAnnotations.size + ' annotations selected)'"
                  @click="selectAllDocuments()">
          <b-icon-square></b-icon-square>
          <span style="width: 30px">&nbsp;</span>
          <span style="width: 3em">&nbsp;</span>
          {{ selectedDocs.size }}
          <b-icon-file-earmark-text></b-icon-file-earmark-text>
          {{ selectedAnnotations.size }}
          <b-icon-pencil-square></b-icon-pencil-square>
        </b-button>
        <b-dropdown>
          <b-dropdown-item @click="selectAllAnnotations()">
            Select all annotations
          </b-dropdown-item>
          <b-dropdown-item @click="clearAnnotationSelection()">
            Clear all annotations
          </b-dropdown-item>
        </b-dropdown>
        <b-button variant="danger" @click="showDeleteConfirmModal = !showDeleteConfirmModal"
                  :disabled="selectedDocs.size < 1 && selectedAnnotations.size < 1"
                  :title="'Delete ' + selectedDocs.size + ' documents and ' + selectedAnnotations.size + ' annotations.'">
          <b-icon-trash-fill scale="1"></b-icon-trash-fill>
          Delete
        </b-button>
        <b-button :variant="loadingVariant" :disabled="isLoading" @click="fetchDocuments">
          <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
          Refresh
        </b-button>
        <b-button variant="primary" @click="uploadHandler" title="Upload documents">
          <b-icon-upload></b-icon-upload>
          Upload
        </b-button>
        <b-button @click="exportHandler" variant="primary">
          <b-icon-download></b-icon-download>
          Export
        </b-button>
      </b-button-group>
    </b-button-toolbar>

    <DeleteModal
        v-model="showDeleteConfirmModal"
        :title="'Delete ' + selectedDocs.size + ' documents and ' + selectedAnnotations.size + ' annotations'"
        @delete="deleteHandler">
      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <p class="badge badge-danger">Deleting a document will also delete their associated annotations.</p>
      <p>Are you sure you want to delete {{ selectedDocs.size }} documents and
        {{ selectedAnnotations.size }} annotations?</p>
    </DeleteModal>

    <Search v-if="showFilters" class="mt-4" @input="searchDocs"></Search>


    <PaginationAsync class="mt-4"
                     v-model="currentPage"
                     :items="documents"
                     :num-items="numTotalDocuments"
                     :items-per-page="itemsPerPage"
                     :is-loading="false"
                     @page-size-change="pageSizeChangeHandler"
                     v-slot:default="{ pageItems }">
      <BCard v-for="doc in pageItems" :key="`${doc.project_id}-${doc.id}`"
             :class="{ 'mb-2': true, 'selectedDoc': isDocSelected(doc)}"
             data-role="document-display-container">
        <BMedia>
          <div class="d-flex justify-content-between">
            <div>
              <div class="mb-2">
                <span @click="toggleDocument(doc)" style="cursor: pointer" class="mr-1">
                  <b-badge variant="primary" :class="{'docBgSelected': isDocSelected(doc)}">
                    <b-icon-file-earmark-check v-if="isDocSelected(doc)"
                                               :class="{ 'docIcon': true, 'docIconSelected': isDocSelected(doc)}"></b-icon-file-earmark-check>
                  <b-icon-file-earmark-text-fill v-else
                                                 :class="{ 'docIcon': true, 'docIconSelected': isDocSelected(doc)}"></b-icon-file-earmark-text-fill>
                  </b-badge>

                </span>

                <strong>
                  <span v-if="doc.doc_id"
                        title="ID of the document. ID is obtained from the field specified in the project's configuration.">{{
                      doc.doc_id
                    }}</span>
                  <b-badge v-else variant="warning" :title="`Specified ID field does not exist in document.`">
                    <b-icon-exclamation-triangle></b-icon-exclamation-triangle>
                  </b-badge>
                </strong>


              </div>
              <div>
                <b-icon-clock class="mr-2"></b-icon-clock>
                {{ doc.created | datetime }}
              </div>
            </div>

            <div>
              <b-badge variant="success" class="mr-2" title="Completed annotations">
                <b-icon-pencil-fill></b-icon-pencil-fill>
                {{ doc.completed }}
              </b-badge>
              <b-badge variant="danger" class="mr-2" title="Rejected annotations">
                <b-icon-x-square-fill></b-icon-x-square-fill>
                {{ doc.rejected }}
              </b-badge>
              <b-badge variant="warning" class="mr-2" title="Timed out annotations">
                <b-icon-clock></b-icon-clock>
                {{ doc.timed_out }}
              </b-badge>
              <b-badge variant="secondary" class="mr-2" title="Aborted annotations">
                <b-icon-stop-fill></b-icon-stop-fill>
                {{ doc.aborted }}
              </b-badge>
              <b-badge variant="primary" class="mr-2" title="Pending annotations">
                <b-icon-play-fill></b-icon-play-fill>
                {{ doc.pending }}
              </b-badge>

            </div>

          </div>


          <div v-if="documentDisplayFormat === 'CSV'" class="mt-2 mb-2 p-2" data-role="document-display-json">
            <b-table :items="jsonToTableData(doc.data)">
              <template #head()="{ column }">
                {{ column }}
              </template>
            </b-table>
          </div>
          <div v-else class="mt-2 mb-2 p-2 data-bg" data-role="document-display-json">
            <vue-json-pretty :data="doc.data"></vue-json-pretty>
          </div>


          <BCard v-for="anno in doc.annotations" :key="anno.id"
                 :class="{ 'mt-4': true, 'selectedAnnotation': isAnnotationSelected(anno)}"
                 data-role="annotation-display-container">

            <BMedia>
              <AnnotationItem :annotation="anno"
                              :document="doc"
                              :project-config="projectConfig"
                              :allow-annotation-edit="allowAnnotationEdit"
                              :selected="isAnnotationSelected(anno)"
                              :allow-change-delete="allowAnnotationChangeDelete"
                              :document-display-format="documentDisplayFormat"
                              @annotation-changed="fetchAnnotation"
                              @selection-changed="toggleAnnotation"
              >
              </AnnotationItem>
            </BMedia>

          </BCard>

        </BMedia>


      </BCard>

    </PaginationAsync>
  </b-overlay>


</template>

<script>
import {mapActions} from "vuex";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import AsyncJsonDisplay from "@/components/AsyncJsonDisplay";
import PaginationAsync from "@/components/PaginationAsync";
import Search from "@/components/Search";
import DeleteModal from "@/components/DeleteModal";
import _ from "lodash"
import {toastError, toastSuccess} from "@/utils";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import AnnotationItem from "@/components/AnnotationItem";
import {flatten} from '@/utils';

/**
 * Displays a list of documents, with builtin pagination.
 *
 * It's the responsibility of the parent component to respond to the `fetch` event to retrieve new
 * data when the page selection changes.
 *
 * Properties
 * documents:array - An array of documents to be displayed
 * isLoading:bool - Toggle showing loading status, cannot interact with the component when loading
 * showMenuBar:bool - Shows the menu bar for performing operations related to documents, e.g. delete, export, etc.
 * showFilters:bool - Show the filtering bar for searching/sorting documents
 * allowAnnotationEdit:bool - Whether to allow user to edit the annotation (make a change in annotation history)
 * allowAnnotationChangeDelete:bool - Whether to allow user to delete an annotation's change history
 *
 * Events
 * fetch(currentPage, pageSize) - The component emits a `fetch` event when page selection changes or refresh
 * button is used.
 * delete({documentIds, annotationIds})
 * upload
 * export({documentIds, annotationIds})
 * selection-changed({documentIds, annotationIds})
 */
export default {
  name: "DocumentsList",
  components: {
    AnnotationItem,
    AnnotationRenderer,
    Search,
    PaginationAsync,
    AsyncJsonDisplay,
    DeleteModal,
    VueJsonPretty
  },
  data() {
    return {
      searchStr: "",
      currentPage: 1,
      itemsPerPage: 10,
      selectedDocs: new Set(),
      selectedAnnotations: new Set(),
      showDeleteConfirmModal: false,
      deleteLocked: true,
    }
  },
  props: {
    /**
     * Documents shown in this page
     */
    documents: {
      default() {
        return []
      }
    },
    /**
     * Total number of documents available
     */
    numTotalDocuments: {
      default: 0,
    },
    /**
     * Displays a loading overlay if true
     */
    isLoading: {
      default: false,
    },
    showMenuBar: {
      default: true,
    },
    showFilters: {
      default: true,
    },
    /**
     * Between json or csv
     */
    documentDisplayFormat: {
      default: "json"
    },
    allowAnnotationEdit: {
      default: false,
    },
    allowAnnotationChangeDelete: {
      default: false
    },
    /**
     * Used for when user requests to edit annotation
     */
    projectConfig: {
      default: null,
    }
  },
  computed: {
    loadingVariant() {
      if (this.isLoading) {
        return "secondary"
      } else {
        return "primary"
      }
    },

  },
  methods: {
    ...mapActions(["getDocumentContent", "getAnnotationContent", "changeAnnotation"]),
    jsonToTableData(data) {
      return [flatten(data)]
    },
    pageSizeChangeHandler(newSize) {
      this.itemsPerPage = newSize
      this.fetchDocuments()
    },
    fetchDocuments() {
      this.$emit("fetch", this.currentPage, this.itemsPerPage)
    },
    fetchAnnotation(annotationId) {
      this.$emit("fetch-annotation", annotationId)
    },
    deleteHandler() {
      this.$emit("delete", this.getSelectionList())
    },
    uploadHandler() {
      this.$emit("upload")
    },
    exportHandler() {
      this.$emit("export", this.getSelectionList())
    },
    getSelectionList() {
      return {
        documentIds: [...this.selectedDocs],
        annotationIds: [...this.selectedAnnotations],
      }
    },
    isPageSelected() {
      for (const doc of this.documents) {
        if (!this.selectedDocs.has(doc.id)) {
          return false
        }
      }
      return true

    },
    searchDocs(searchStr) {
      this.searchStr = searchStr
    },
    emitSelectionList() {
      // Forces vue to track the set change
      this.selectedDocs = new Set(this.selectedDocs)
      this.selectedAnnotations = new Set(this.selectedAnnotations)

      this.$emit("selection-changed", this.getSelectionList())
    },
    selectDocument(doc, doSelect, emitEvent = true) {
      if (doSelect) {
        this.selectedDocs.add(doc.id)
        for (let anno of doc.annotations) {
          this.selectedAnnotations.add(anno.id)
        }
      } else {
        this.selectedDocs.delete(doc.id)
        for (let anno of doc.annotations) {
          this.selectedAnnotations.delete(anno.id)
        }
      }

      if (emitEvent)
        this.emitSelectionList()

    },
    toggleDocument(doc) {
      this.selectDocument(doc, !this.selectedDocs.has(doc.id))
    },
    isDocSelected(doc) {
      return this.selectedDocs.has(doc.id)
    },
    selectAnnotation(anno, doSelect, doc, emitEvent = true) {
      //Can't change selection if document is already selected
      if (this.isDocSelected(doc))
        return

      if (doSelect)
        this.selectedAnnotations.add(anno.id)
      else
        this.selectedAnnotations.delete(anno.id)


      if (emitEvent)
        this.emitSelectionList()

    },
    toggleAnnotation(anno, doc) {
      this.selectAnnotation(anno, !this.selectedAnnotations.has(anno.id), doc)
    },
    isAnnotationSelected(anno) {
      return this.selectedAnnotations.has(anno.id)
    },
    clearDocumentSelection(doEmitEvent = true) {
      for (let doc of this.documents) {
        this.selectDocument(doc, false, false)
      }
      if (doEmitEvent)
        this.emitSelectionList()
    },
    clearAnnotationSelection(doEmitEvent = true) {
      for (let doc in this.documents) {
        for (let anno in doc.annotations) {
          this.selectAnnotation(anno, false, doc, false)
        }
      }

      if (doEmitEvent)
        this.emitSelectionList()

    },
    selectAllDocuments(doEmitEvent = true) {
      for (let doc of this.documents) {
        this.selectDocument(doc, true, false)
      }

      if (doEmitEvent)
        this.emitSelectionList()

    },
    selectAllAnnotations(doEmitEvent = true) {
      for (let doc of this.documents) {
        for (let anno of doc.annotations) {
          this.selectAnnotation(anno, true, doc, false)
        }
      }
      if (doEmitEvent)
        this.emitSelectionList()
    },
  },
  watch: {
    currentPage: {
      handler() {
        this.fetchDocuments()
      }
    }
  },
  mounted() {
    this.fetchDocuments()

  }
}
</script>

<style scoped>

.selectedDoc {
  background: #cbcbcb;
}

.selectedAnnotation {
  background: #b3b3b3;
}

.docBgSelected {
  background: #fff;
}

.docIcon {
  width: 1.5em;
  height: auto
}

.docIconSelected {
  color: black;
}

</style>
