<template>
  <div class="container">
    <h1>Project</h1>
    <b-form class="mt-4 mb-4">

      <b-form-group label="Name">
        <b-form-input v-model="local_project.name"></b-form-input>
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
      <VTable :data="documents" :column-display="tableColumnsDisplay" :column-ignore="tableIgnoreColumns"></VTable>
    </div>

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
    ...mapActions(["getProjects", "updateProject","getProjectDocuments"]),
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
