<template>
  <div>
    <h2 class="mt-2 mb-2">Documents & Annotations
      <b-icon-question-circle id="project-documents-help" scale="0.5"
                              style="cursor:pointer;"></b-icon-question-circle>
    </h2>
    <b-popover target="project-documents-help" triggers="hover" placement="bottom">
      You can view the list of documents and annotations of this project in this tab.
      Start by <a href="#" @click.prevent="uploadBtnHandler">uploading</a> documents to the project,
      documents must be in a JSON format. Annotators can then be recruited by using the <a href="#"
                                                                                           @click.prevent="activeTab = 2">Annotators</a>
      page.

    </b-popover>
    <div v-if="project && project.id">
      <b-button-toolbar class="mt-2 mb-2">
      <b-button-group>
        <b-button v-if="isEverythingSelected()"
                  :title="'Clear selection. (' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations selected)'"
                  @click="$refs.docsList.clearDocumentSelection()">
          <b-icon-check-square></b-icon-check-square>
          <span style="width: 30px">&nbsp;</span>
          {{ selectedDocuments.length }}
          <b-icon-file-earmark-text></b-icon-file-earmark-text>
          {{ selectedAnnotations.length }}
          <b-icon-pencil-square></b-icon-pencil-square>
        </b-button>
        <b-button v-else
                  :title="'Select all (' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations selected)'"
                  @click="$refs.docsList.selectAllDocuments()">
          <b-icon-square></b-icon-square>
          <span style="width: 30px">&nbsp;</span>
          <span style="width: 3em">&nbsp;</span>
          {{ selectedDocuments.length }}
          <b-icon-file-earmark-text></b-icon-file-earmark-text>
          {{ selectedAnnotations.length }}
          <b-icon-pencil-square></b-icon-pencil-square>
        </b-button>
        <b-dropdown>
          <b-dropdown-item @click="$refs.docsList.selectAllAnnotations()">
            Select all annotations
          </b-dropdown-item>
          <b-dropdown-item @click="$refs.docsList.clearAnnotationSelection()">
            Clear all annotations
          </b-dropdown-item>
        </b-dropdown>
        <b-button variant="danger" @click="showDeleteConfirmModal = !showDeleteConfirmModal"
                  :disabled="selectedDocuments.length < 1 && selectedAnnotations.length < 1"
                  :title="'Delete ' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations.'">
          <b-icon-trash-fill scale="1"></b-icon-trash-fill>
          Delete
        </b-button>
        <b-button :variant="loadingVariant" :disabled="loading" @click="refreshDocumentsHandler">
          <b-icon-arrow-clockwise :animation="loadingIconAnimation"></b-icon-arrow-clockwise>
          Refresh
        </b-button>
        <b-button variant="primary" @click="showDocumentUploadModal = true" title="Upload documents">
          <b-icon-upload></b-icon-upload>
          Upload
        </b-button>
        <b-button @click="showDocumentExportModal = true" variant="primary">
          <b-icon-download></b-icon-download>
          Export
        </b-button>
      </b-button-group>


    </b-button-toolbar>

    <DocumentUploader v-model="showDocumentUploadModal"
                      :project-id="project.id"
                      @uploading="documentStartUploadHandler"
                      @completed="documentUploadHandler"></DocumentUploader>

    <DocumentExporter v-model="showDocumentExportModal"
                      :project-id="project.id">
    </DocumentExporter>

    <b-modal v-model="showDeleteConfirmModal"
             ok-variant="danger"
             ok-title="Delete"
             :ok-disabled="deleteLocked"
             @ok="deleteDocumentsAndAnnotationHandler"
             @hidden="deleteLocked = true"
             :title="'Delete ' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations'">

      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <p class="badge badge-danger">Deleting a document will also delete their associated annotations.</p>

      <p>Are you sure you want to delete {{ selectedDocuments.length }} documents and
        {{ selectedAnnotations.length }} annotations?</p>

      <div>
        <b-button @click="deleteLocked = !deleteLocked"
                  :class="{'btn-danger': deleteLocked, 'btn-success': !deleteLocked}"
        >
          <b-icon-lock-fill v-if="deleteLocked"></b-icon-lock-fill>
          <b-icon-unlock-fill v-else></b-icon-unlock-fill>
          <span v-if="deleteLocked">Unlock delete</span>
          <span v-else>Lock delete</span>
        </b-button>

      </div>
    </b-modal>


    <div v-if="documents">
      <b-overlay :show="loading">
        <DocumentsList ref="docsList" :documents="documents"
                       @selection-changed="docAnnoSelectionChanged"></DocumentsList>
      </b-overlay>
    </div>
    <div v-else>
      No documents uploaded
    </div>

    </div>
    <div v-else>
      No valid project to display documents
    </div>


  </div>
</template>

<script>
import {mapActions, mapState} from "vuex";
import DocumentExporter from "@/components/DocumentExporter";
import DocumentUploader from "@/components/DocumentUploader";
import DocumentsList from "@/components/DocumentsList";
import {toastError, toastSuccess} from "@/utils";


export default {
  name: "ProjectDocuments",
  components: {
    DocumentExporter,
    DocumentUploader,
    DocumentsList,
  },
  data() {
    return {
      documents: [],
      selectedDocuments: [],
      selectedAnnotations: [],
      showDeleteConfirmModal: false,
      showDocumentUploadModal: false,
      showDocumentExportModal: false,
      deleteLocked: true,
      loading: false,

    }
  },
  props: {
    project: {
      default: null,
    }
  },
  computed: {
    loadingVariant() {
      if (this.loading) {
        return "secondary"
      } else {
        return "primary"
      }
    },
    loadingIconAnimation() {
      if (this.loading) {
        return "throb"
      }

      return null
    },
  },
  methods: {
    ...mapActions(["getProjectDocuments", "addProjectDocument",
      "deleteDocumentsAndAnnotations",]),
    async updateProjectDocuments() {
      if (this.project && this.project.id) {
        this.documents = await this.getProjectDocuments(this.project.id)
      }

    },
    async refreshDocumentsHandler() {
      this.setLoading(true)
      try {
        this.documents = await this.getProjectDocuments(this.project.id)
      } catch (e) {
        toastError(this, "Could not reload document", e)
      }
      this.setLoading(false)
    },
    async documentStartUploadHandler(e) {
      this.setLoading(true)
    },
    async documentUploadHandler(e) {
      await this.fetchProject()
      this.setLoading(false)
    },
    docAnnoSelectionChanged(value) {
      this.selectedDocuments = value.documents
      this.selectedAnnotations = value.annotations
    },
    isEverythingSelected() {
      return this.selectedDocuments.length >= this.numDocs &&
          this.selectedAnnotations.length >= this.numAnnotations
    },
    async deleteDocumentsAndAnnotationHandler(e) {
      try {
        await this.deleteDocumentsAndAnnotations({
          documentIds: this.selectedDocuments,
          annotationIds: this.selectedAnnotations
        })
        toastSuccess(this, "Documents and annotations deleted", this.selectedDocuments.length + "documents and " + this.selectedAnnotations.length + "deleted.")

        await this.refreshDocumentsHandler()

      } catch (e) {
        toastError(this, "Could not delete documents or annotations", e)

      }

    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
  },
  watch: {
    project: {
      immediate: true,
      handler(newValue) {
        this.updateProjectDocuments()
      }
    }
  },
  async mounted() {
    this.updateProjectDocuments()
  }

}
</script>

<style scoped>

</style>
