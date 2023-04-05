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

      <b-button-toolbar class="mt-4">
        <b-button-group>
          <b-button @click="showDeleteProjectModal=true" variant="danger" :disabled="loading"
                  title="Delete project." size="sm">
          <b-icon-x></b-icon-x>
          Delete project
        </b-button>

        </b-button-group>
      </b-button-toolbar>

    </b-card>

    <DeleteModal v-model="showDeleteProjectModal"
                 :title="'Delete project #' + local_project.id + ' ' + local_project.name +  '?'"
                 @delete="deleteProjectHandler"
    >
      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <p class="badge badge-danger">Deleting a project will also delete all associated documents and annotations.</p>
    </DeleteModal>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">
        <ProjectConfiguration :project="local_project" @updated="fetchProject()"></ProjectConfiguration>
      </b-tab>
      <b-tab title="Documents & Annotations">
        <ProjectDocumentsManager :project="local_project" @updated="fetchProject()"></ProjectDocumentsManager>
      </b-tab>
      <b-tab title="Annotators" :disabled="!local_project.is_configured">
        <Annotators :project="local_project" @updated="fetchProject()"></Annotators>
      </b-tab>

      <b-tab title="Statistics">
        <AnnotationStatistics :projectId="projectId"></AnnotationStatistics>
      </b-tab>

    </b-tabs>
  </div>
</template>
<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";

import Annotators from "@/components/Annotators.vue";

import {readFileAsync, toastError, toastSuccess} from "@/utils";

import ProjectIcon from "@/components/ProjectIcon.vue";
import ProjectStatusBadges from "@/components/ProjectStatusBadges.vue";

import AnnotationStatistics from "@/components/AnnotationStatistics.vue";
import ProjectConfiguration from "@/components/ProjectConfiguration.vue";
import ProjectDocumentsManager from "@/components/ProjectDocumentsManager.vue";
import DeleteModal from "@/components/DeleteModal.vue";

export default {
  name: "Project",
  title() {
    return `Project`
  },
  components: {
    DeleteModal,
    ProjectDocumentsManager,
    ProjectConfiguration,
    ProjectStatusBadges,
    ProjectIcon,
    Annotators, AnnotationStatistics},
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
      showDeleteProjectModal: false,
      deleteProjectLocked: true,
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
    ...mapActions(["getProject","deleteProject"]),
    async fetchProject() {
      try {
        if (this.projectId) {
          this.local_project = await this.getProject(this.projectId)
          // this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError("Could not fetch project information from server", undefined, this)
      }

    },

    async setLoading(isLoading) {
      this.loading = isLoading
    },

    goToAnnotatePage(e) {
      this.$router.push(`/annotate/${this.projectId}/${this.documents[0].id}`)

    },
    async deleteProjectHandler(){
      try{
        await this.deleteProject(this.local_project.id)
        toastSuccess("Project deleted", "The project has been deleted", null)
        this.$router.push("/projects")
      }catch(e){
        toastError("Could not delete project", e, null)
      }
    },




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
