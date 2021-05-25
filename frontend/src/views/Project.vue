<template>
  <div class="container">
    <h1>Project</h1>
    <b-form class="mt-4 mb-4">

      <b-form-group label="Name">
        <b-form-input v-model="local_project.name" name="project_name"></b-form-input>
      </b-form-group>

      <b-form-row>
        <b-col>
          <JsonEditor v-model="local_project.configuration"></JsonEditor>
        </b-col>
        <b-col>
          <strong>Annotation preview</strong>
          <AnnotationRenderer :config="local_project.configuration"></AnnotationRenderer>
        </b-col>
      </b-form-row>
    <b-form-group label="Documents" class="mt-4">
      <b-file @change="fileHandler" multiple></b-file>
    </b-form-group>

      <b-form-row>
        <b-col>
          <b-button @click="saveProjectHandler">Save</b-button>
        </b-col>
      </b-form-row>
    </b-form>

    <div v-if="documents">
      <VTable :data="documents" :column-display="tableColumnsDisplay" :column-ignore="tableIgnoreColumns" :allowExport="false"></VTable>
    </div>

    <b-button variant="primary" @click="exportAnnotationsHandler">
        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor"
           xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd"
              d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
        <path fill-rule="evenodd"
              d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
      </svg>
      Export Annotations (JSON)</b-button>

  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import VTable from "@/components/VTable";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import JsonEditor from "@/components/JsonEditor";

export default {
  name: "Project",
  components: {JsonEditor, AnnotationRenderer, VTable},
  data() {
    return {
      local_project: {
        name: null,
        configuration: null,
        data: null,
      },
      configurationStr: "",
      documents: null,
      tableColumnsDisplay: {
        'id': 'string',
        'text':'string',
      },
      tableIgnoreColumns: ['annotations','project','data'],
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.id
    },
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
  async mounted(){
    await this.getProjects();
    this.documents = await this.getProjectDocuments(this.projectId);
  }
}
</script>

<style scoped>

</style>
