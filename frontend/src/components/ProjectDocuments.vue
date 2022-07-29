<template>
  <div v-if="project && project.id">
    <DocumentsList ref="docsList"
                   :documents="documents"
                   :num-total-documents="numTotalDocuments"
                   :is-loading="loading"
                   :allow-annotation-edit="project.allow_annotation_change"
                   :project-config="project.configuration"
                   @fetch="refreshDocumentsHandler"
                   @fetch-annotation="refreshAnnotationHandler"
                   @upload="showDocumentUploadModal = true"
                   @delete="deleteDocumentsAndAnnotationHandler"
                   @export="showDocumentExportModal = true"
    >
    </DocumentsList>

    <DocumentUploader v-model="showDocumentUploadModal"
                      :project-id="project.id"
                      @uploading="documentStartUploadHandler"
                      @completed="documentUploadHandler"></DocumentUploader>

    <DocumentExporter v-model="showDocumentExportModal"
                      default-doc-type="annotation"
                      :project-id="project.id">
    </DocumentExporter>
  </div>
</template>

<script>
import {mapActions, mapState} from "vuex";
import DocumentExporter from "@/components/DocumentExporter";
import DocumentUploader from "@/components/DocumentUploader";
import DocumentsList from "@/components/DocumentsList";
import {toastError, toastSuccess} from "@/utils";
import DeleteModal from "@/components/DeleteModal";


export default {
  name: "ProjectDocuments",
  components: {
    DeleteModal,
    DocumentExporter,
    DocumentUploader,
    DocumentsList,
  },
  data() {
    return {
      documents: [],
      numTotalDocuments: 0,
      selectedDocuments: [],
      selectedAnnotations: [],
      showDeleteConfirmModal: false,
      showDocumentUploadModal: false,
      showDocumentExportModal: false,
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
    numDocs() {
      return this.documents.length
    },
    numAnnotations() {
      let numAnnotations = 0
      for (let doc of this.documents) {
        numAnnotations += doc.annotations.length
      }

      return numAnnotations
    }

  },
  methods: {
    ...mapActions(["getProjectDocuments", "addProjectDocument", "getAnnotation",
      "deleteDocumentsAndAnnotations"]),
    isEverythingSelected() {
      return this.selectedDocuments.length >= this.numDocs &&
          this.selectedAnnotations.length >= this.numAnnotations
    },
    async refreshDocumentsHandler(currentPage, pageSize) {
      this.setLoading(true)

      try {
        const result = await this.getProjectDocuments({
          project_id: this.project.id,
          current_page: currentPage,
          page_size: pageSize,
        })
        this.documents = result.items
        this.numTotalDocuments = result.total_count
        this.$emit("updated")
      } catch (e) {
        toastError("Could not reload document", e, this)
      }
      this.setLoading(false)
    },
    async refreshAnnotationHandler(annotationId) {
      this.setLoading(true)

      try {
        const result = await this.getAnnotation(annotationId)

        function replaceDocAnnotation(documents) {
          for (let i = 0; i < documents.length; i++) {
            for (let j = 0; j < documents[i].annotations.length; j++) {
              if (documents[i].annotations[j].id === annotationId) {
                // Replace
                documents[i].annotations[j] = result
                return
              }
            }
          }
        }
        replaceDocAnnotation(this.documents)


        this.$emit("updated")
      } catch (e) {
        toastError("Could not reload annotation", e, this)
      }


      this.setLoading(false)

    },
    async documentStartUploadHandler(e) {

    },
    async documentUploadHandler(e) {
      this.$refs.docsList.fetchDocuments()
      this.$emit("updated")
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
    async deleteDocumentsAndAnnotationHandler({documentIds, annotationIds}) {
      try {
        await this.deleteDocumentsAndAnnotations({
          documentIds: documentIds,
          annotationIds: annotationIds
        })
        toastSuccess("Documents and annotations deleted", documentIds.length + "documents and " + annotationIds.length + "deleted.", this)

        this.$refs.docsList.fetchDocuments()

      } catch (e) {
        toastError("Could not delete documents or annotations", e, this)

      }

    },
  },

}
</script>

<style scoped>

</style>
