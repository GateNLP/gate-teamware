<template>
  <div class="container pt-2">
    <h1>
      <ProjectIcon :project-id="projectId"></ProjectIcon>
      {{ local_project.name }}
    </h1>

    <b-card class="mt-2 mb-2">
      <h4>Project overview</h4>
      <p class="form-text text-muted">
        Current status of the project.
      </p>
      <ProjectStatusBadges :project="local_project"></ProjectStatusBadges>


      <div v-if="!local_project.is_configured" class="alert alert-warning mt-2" >
        <b-icon-exclamation-triangle></b-icon-exclamation-triangle>
        Improperly configured project:
        <ul>
          <li v-for="message in local_project.configuration_error">{{ message }}</li>
        </ul>
      </div>
      <div v-else-if="local_project.is_completed" class="alert alert-success mt-2" >
        <b-icon-check-square></b-icon-check-square> All annotation tasks in this project are completed.
      </div>

    </b-card>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">
        <ProjectConfiguration :project="local_project" @updated="fetchProject()"></ProjectConfiguration>
      </b-tab>

      <b-tab title="Documents & Annotations">
        <ProjectDocuments :project="local_project"></ProjectDocuments>
      </b-tab>

      <b-tab title="Annotators" :disabled="!local_project.is_configured">
        <h2 class="mt-2 mb-2">Annotators Management
          <b-icon-question-circle id="project-annotators-help" scale="0.5"
                                  style="cursor:pointer;"></b-icon-question-circle>
        </h2>
        <b-popover target="project-annotators-help" triggers="hover" placement="bottom">
          Add annotators to the project by clicking on the list of names in the <strong>right column</strong>. Current
          annotators can be removed
          by clicking on the names in the <strong>left column</strong>. Removing annotators does not delete their
          completed annotations
          but will stop their current pending annotation task.

        </b-popover>
        <b-button-toolbar class="mt-2 mb-2">
          <b-button-group>
            <b-button :variant="loadingVariant" :disabled="loading" @click="refreshAnnotatorsHandler" title="Refresh annotator list.">
              <b-icon-arrow-clockwise :animation="loadingIconAnimation"></b-icon-arrow-clockwise>
              Refesh
            </b-button>
          </b-button-group>
        </b-button-toolbar>
        <Annotators :projectID="projectId" ref="annotators"></Annotators>
      </b-tab>

    </b-tabs>


  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import VTable from "@/components/VTable";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import Annotators from "@/components/Annotators";
import JsonEditor from "@/components/JsonEditor";
import VJsoneditor from "v-jsoneditor";
import {readFileAsync, toastError, toastSuccess} from "@/utils";
import DocumentsList from "@/components/DocumentsList";
import MarkdownEditor from "@/components/MarkdownEditor";
import ProjectIcon from "@/components/ProjectIcon";
import ProjectStatusBadges from "@/components/ProjectStatusBadges";
import DocumentUploader from "@/components/DocumentUploader";
import DocumentExporter from "@/components/DocumentExporter";
import ProjectConfiguration from "@/components/ProjectConfiguration";
import ProjectDocuments from "@/components/ProjectDocuments";

export default {
  name: "Project",
  title() {
    return `Project - ${this.local_project.name}`
  },
  components: {
    ProjectDocuments,
    ProjectConfiguration,
    DocumentExporter,
    DocumentUploader,
    ProjectStatusBadges,
    ProjectIcon,
    MarkdownEditor, DocumentsList, JsonEditor, AnnotationRenderer, VTable, VJsoneditor, Annotators},
  data() {
    return {
      activeTab: 0,
      annotationOutput: {},
      local_project: {
        name: null,
        description: "",
        annotator_guideline: "",
        configuration: null,
        data: null,
        annotations_per_doc: 3,
        annotator_max_annotation: 0.6,
        allow_document_reject: true,
        document_input_preview: {},
        is_configured: false,
        is_completed: false,
        document_id_field: "",
      },
      configurationStr: "",
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
    projectId: {
      type: String,
    }

  },
  computed: {
    ...mapState(["projects"]),
    projectConfigValid() {
      return this.local_project && this.local_project.configuration && this.local_project.configuration.length > 0
    },
    projectReadyForAnnotation() {
      return this.projectConfigValid()
    },
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
    ...mapActions(["getProject",]),
    async fetchProject() {
      try {
        if (this.projectId) {
          this.local_project = await this.getProject(this.projectId)
          // this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError(this, "Could not fetch project information from server")
      }

    },

    async setLoading(isLoading) {
      this.loading = isLoading
    },

    goToAnnotatePage(e) {
      this.$router.push(`/annotate/${this.projectId}/${this.documents[0].id}`)

    },


    async refreshAnnotatorsHandler(){
      this.$refs.annotators.updateAnnotators()
    }

  },
  watch: {
    projectId: {
      immediate: true,
      handler() {
        this.fetchProject()
      }
    },
  },
  async beforeMount() {
    this.fetchProject()


  },
}
</script>

<style scoped>

.infoCard {
  background: #838383;
  color: white;
  margin: 1em 0;

}


</style>
