<template>
  <div class="container">
    <h1>Project: {{ local_project.name }}</h1>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">

        <h2 class="mt-2 mb-2">Project configuration</h2>
        <b-form class="mt-4 mb-4">
          <b-form-group label="Name">
            <b-form-input v-model="local_project.name" name="project_name"></b-form-input>
          </b-form-group>
          <b-form-group label="Description">
            <b-textarea v-model="local_project.description" name="project_description"></b-textarea>
          </b-form-group>
          <b-form-group label="Annotations per document">
            <b-form-input v-model="local_project.annotations_per_doc"></b-form-input>
          </b-form-group>
          <b-form-group label="Maximum percentage of documents annotated per annotator">
            <b-form-input v-model="local_project.annotator_max_annotation"></b-form-input>
          </b-form-group>
          <b-form-row>
            <b-col>
              <h4>Annotation configuration</h4>
              <JsonEditor v-model="local_project.configuration"></JsonEditor>
            </b-col>
            <b-col>
              <h4>Annotation preview</h4>
              <AnnotationRenderer :config="local_project.configuration"
                                  @input="annotationOutputHandler"></AnnotationRenderer>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <h5 class="mt-4">Document input preview</h5>
              <VJsoneditor v-model="testDocument" :options="{mode: 'code'}" :plus="false" height="400px"></VJsoneditor>
            </b-col>
            <b-col>
              <h5 class="mt-4">Annotation output preview</h5>
              <VJsoneditor v-model="annotationOutput" :options="{mode: 'preview', mainMenuBar: false}" :plus="false"
                           height="400px"></VJsoneditor>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col class="mt-4">
              <b-button @click="saveProjectHandler" :variant="loadingVariant" :disabled="loading">
                <b-icon-box-arrow-in-down :animation="loadingIconAnimation"></b-icon-box-arrow-in-down>
                Save project configuration
              </b-button>
            </b-col>
          </b-form-row>
        </b-form>


      </b-tab>
      <b-tab title="Documents & Annotations">
        <h2 class="mt-2 mb-2">Documents & Annotations</h2>

        <b-button-toolbar class="mt-2 mb-2">
          <b-button variant="primary" @click="exportAnnotationsHandler" class="mr-2">
            <b-icon-download></b-icon-download>
            Export Annotations (JSON)
          </b-button>
          <b-button variant="primary" @click="uploadBtnHandler" class="mr-2">
            <b-icon-upload></b-icon-upload>
            Upload documents
          </b-button>
          <b-button :variant="loadingVariant" :disabled="loading" @click="refreshDocumentsHandler" class="mr-2">
            <b-icon-arrow-clockwise :animation="loadingIconAnimation"></b-icon-arrow-clockwise>
            Refresh documents
          </b-button>
          <input ref="documentUploadInput" type="file" @change="documentUploadHandler" multiple hidden/>
        </b-button-toolbar>


        <div v-if="documents">
          <b-overlay :show="loading">
            <DocumentsList :documents="documents"></DocumentsList>
          </b-overlay>
        </div>
        <div v-else>
          No documents uploaded
        </div>
      </b-tab>
      <b-tab title="Annotators">
        <h2 class="mt-2 mb-2">Annotators Management</h2>
        <Annotators :projectID="projectId"></Annotators>
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

export default {
  name: "Project",
  components: {DocumentsList, JsonEditor, AnnotationRenderer, VTable, VJsoneditor, Annotators},
  data() {
    return {
      activeTab: 0,
      testDocument: {
        text: "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"
      },
      annotationOutput: {},
      local_project: {
        name: null,
        configuration: null,
        data: null,
        annotations_per_doc: 3,
        annotator_max_annotation: 0.6,
      },
      configurationStr: "",
      documents: null,

      loading: false,
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.id
    },
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
    }

  },
  methods: {
    ...mapActions(["getProjects", "updateProject", "getProjectDocuments", "getAnnotations", "addProjectDocument"]),
    async refreshDocumentsHandler() {
      this.setLoading(true)
      try {
        this.documents = await this.getProjectDocuments(this.projectId)
      } catch (e) {
        toastError(this, "Could not reload document", e)
      }
      this.setLoading(false)
    },
    async saveProjectHandler() {
      this.setLoading(true)
      try {
        await this.updateProject(this.local_project);
        this.documents = await this.getProjectDocuments(this.projectId)
        toastSuccess(this, "Save project configuration", "Save successful")
      } catch (e) {
        toastError(this, "Could not save project configuration", e)
      }
      this.setLoading(false)
    },
    async uploadBtnHandler() {
      console.log(this.$refs)
      this.$refs.documentUploadInput.click()
    },
    async documentUploadHandler(e) {

      this.setLoading(true)
      try {
        const fileList = e.target.files

        for (let file of fileList) {
          try {
            const documentsStr = await readFileAsync(file)
            const documents = JSON.parse(documentsStr)
            // Uploaded file must be an array of docs
            if (documents instanceof Array) {
              for (let document of documents) {
                await this.addProjectDocument({projectId: this.projectId, document: document})
              }
            }

          } catch (e) {
            console.error("Could not parse uploaded file")
            console.error(e)
            toastError(this, "Could not parse uploaded file " + file, e)
          }

          this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError(this, "Could not upload document", e)
      }

      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
    async exportAnnotationsHandler() {
      let response = await this.getAnnotations(this.projectId)
      let fileURL = window.URL.createObjectURL(new Blob([response]));
      let fileLink = document.createElement('a');


      fileLink.href = fileURL;
      fileLink.setAttribute('download', 'annotations.json');
      document.body.appendChild(fileLink);

      fileLink.click();

    },
    goToAnnotatePage(e) {
      this.$router.push(`/annotate/${this.projectId}/${this.documents[0].id}`)

    },
    annotationOutputHandler(value) {
      this.annotationOutput = value
    }

  },
  watch: {
    projects: {
      immediate: true,
      handler(newProjectsList) {
        if (this.projectId && newProjectsList) {
          for (let project of newProjectsList) {
            if (String(project.id) === this.projectId) {
              this.local_project = _.cloneDeep(project)

            }
          }
        }
      }
    },
  },
  async mounted() {
    await this.getProjects();
    this.documents = await this.getProjectDocuments(this.projectId);
  }
}
</script>

<style scoped>

</style>
