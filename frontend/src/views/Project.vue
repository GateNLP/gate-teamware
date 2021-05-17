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
import VTable from "../components/VTable";
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
    ...mapActions(["getProjects", "updateProject", "getProjectDocuments"]),
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
