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
      <b-tabs pills card>
        <b-tab title="Annotation Documents" >
          <ProjectDocuments :project="project"  @updated="docsUpdatedHandler"></ProjectDocuments>
        </b-tab>
        <b-tab title="Training Documents" :disabled="!project.has_training_stage">
          <ProjectTrainingDocuments :project="project" @updated="docsUpdatedHandler"></ProjectTrainingDocuments>
        </b-tab>
        <b-tab title="Testing Documents" :disabled="!project.has_test_stage">
          <ProjectTestDocuments :project="project" @updated="docsUpdatedHandler"></ProjectTestDocuments>
        </b-tab>
      </b-tabs>

    </div>
  </div>
</template>

<script>
import {mapActions, mapState} from "vuex";
import DocumentExporter from "@/components/DocumentExporter.vue";
import DocumentUploader from "@/components/DocumentUploader.vue";
import DocumentsList from "@/components/DocumentsList.vue";
import {toastError, toastSuccess} from "@/utils";
import DeleteModal from "@/components/DeleteModal.vue";
import ProjectDocuments from "@/components/ProjectDocuments.vue";
import ProjectTrainingDocuments from "@/components/ProjectTrainingDocuments.vue";
import ProjectTestDocuments from "@/components/ProjectTestDocuments.vue";


export default {
  name: "ProjectDocumentsManager",
  components: {
    ProjectTestDocuments,
    ProjectTrainingDocuments,
    ProjectDocuments,
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
    ...mapActions(["getProjectDocuments", "addProjectDocument",
      "deleteDocumentsAndAnnotations",]),
   docsUpdatedHandler(){
      this.$emit("updated")
   }
  },

}
</script>

<style scoped>

</style>
