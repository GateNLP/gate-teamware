<template>
  <div class="container">
    <h1>Project</h1>
    <b-form>

      <b-form-group label="Name">
        <b-form-input v-model="local_project.name"></b-form-input>
      </b-form-group>

      <b-form-group label="Project Configuration">
        <b-textarea v-model="local_project.configuration"></b-textarea>
      </b-form-group>
      <div class="text-danger" v-if="local_project.configuration && json_error && valid_json == false">{{ json_error }}</div>
      <div class="text-success" v-if="valid_json == true">Valid JSON ✔</div>

    <b-form-group label="Documents" class="mt-4">
      <b-file @change="fileHandler" multiple></b-file>
    </b-form-group>

      <b-form-row>
        <b-col>
          <b-button @click="saveProjectHandler">Save</b-button>
        </b-col>
      </b-form-row>
    </b-form>

    <div>
      {{ local_project.data }}
    </div>

    <div v-if="documents">
      <VTable :data="documents" :column-display="tableColumnsDisplay"></VTable>
    </div>

  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import VTable from "../components/VTable";

export default {
  name: "Project",
  components: {VTable},
  data() {
    return {
      local_project: {
        name: null,
        configuration: null,
        data: null,
      },
      valid_json: null,
      json_error: "",
      documents: null,
      tableColumnsDisplay: {
        'id': 'string',
        'text':'string',
    },
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.id
    },
  },
  methods: {
    ...mapActions(["updateProject","getProjectDocuments"]),
    async saveProjectHandler() {
      this.updateProject(this.local_project);
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
    validateJSON(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            this.json_error = JSON.stringify(e.message);
            return false;
        }
        return true;
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
    local_project: {
      handler(newValue, oldValue) {
        this.valid_json = this.validateJSON(newValue.configuration);
      },
      deep: true,
    }
  },
  async mounted(){
    this.documents = await this.getProjectDocuments(this.projectId);
  }
}
</script>

<style scoped>

</style>
