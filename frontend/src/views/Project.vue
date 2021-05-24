<template>
  <div class="container">
    <h1>Project: {{local_project.name}}</h1>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">
        <b-form class="mt-4 mb-4">
          <b-form-group label="Name">
            <b-form-input v-model="local_project.name"></b-form-input>
          </b-form-group>
          <b-form-row>
            <b-col>
              <h4>Project configuration</h4>
              <JsonEditor v-model="local_project.configuration"></JsonEditor>

              <h5 class="mt-4">Document input preview</h5>
              <VJsoneditor v-model="testDocument" :options="{mode: 'code'}" :plus="false" height="400px"></VJsoneditor>

            </b-col>
            <b-col>
              <h4>Annotation preview</h4>
              <AnnotationRenderer :config="local_project.configuration" @input="annotationOutputHandler"></AnnotationRenderer>

              <h5 class="mt-4">Annotation output preview</h5>
              <VJsoneditor v-model="annotationOutput" :options="{mode: 'preview', mainMenuBar: false}" :plus="false" height="400px" ></VJsoneditor>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col class="mt-4">
              <b-button @click="saveProjectHandler" variant="primary"><b-icon-box-arrow-in-down></b-icon-box-arrow-in-down> Save project configuration</b-button>
            </b-col>
          </b-form-row>
        </b-form>
      </b-tab>
      <b-tab title="Documents" :disabled="documentTabDisabled">

        <b-button variant="primary" v-if="local_project.configuration && documents && documents.length > 0" @click="goToAnnotatePage">Annotate documents</b-button>
        
        <b-button variant="primary" @click="exportAnnotationsHandler">
        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor"
           xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd"
              d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
        <path fill-rule="evenodd"
              d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
        </svg>
        Export Annotations (JSON)</b-button>

        <b-form>
          <b-form-group label="Documents" class="mt-4">
            <b-file @change="fileHandler" multiple></b-file>
          </b-form-group>

          <div v-if="documents">
            <VTable :data="documents" :column-display="tableColumnsDisplay"></VTable>
          </div>
        </b-form>
      </b-tab>

    </b-tabs>


  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import VTable from "@/components/VTable";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import JsonEditor from "@/components/JsonEditor";
import VJsoneditor from "v-jsoneditor";

export default {
  name: "Project",
  components: {JsonEditor, AnnotationRenderer, VTable, VJsoneditor},
  data() {
    return {
      activeTab: 0,
      testDocument: {
          text: "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"
        },
      annotationOutput: {

      },
      local_project: {
        name: null,
        configuration: null,
        data: null,
      },
      configurationStr: "",
      documents: null,
      tableColumnsDisplay: {
        'id': 'string',
        'text': 'string',
      },
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.id
    },
    documentTabDisabled(){
      return !(this.local_project && this.local_project.configuration && this.local_project.configuration.length > 0)
    }
  },
  methods: {
    ...mapActions(["getProjects", "updateProject","getProjectDocuments", "getAnnotations"]),
    async saveProjectHandler() {
      await this.updateProject(this.local_project);
      this.documents = await this.getProjectDocuments(this.projectId);
    },
    fileHandler(e) {
      const self = this
      const fileList = e.target.files
      self.local_project.data = '';
      for (let file of fileList) {
        const reader = new FileReader()
        reader.onload = function (e) {
          console.log(e.target.result)
          self.local_project.data += e.target.result
        }
        reader.readAsText(file)
      }
    },
    async exportAnnotationsHandler(){
        this.getAnnotations(this.projectId)
        .then((response) => {
            var fileURL = window.URL.createObjectURL(new Blob([response]));
            var fileLink = document.createElement('a');


            fileLink.href = fileURL;
            fileLink.setAttribute('download', 'annotations.json');
            document.body.appendChild(fileLink);

            fileLink.click();
          });
    },
    goToAnnotatePage(e){
      this.$router.push(`/annotate/${this.projectId}/${this.documents[0].id}`)

    },
    annotationOutputHandler(value){
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
