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

      <b-form-row>
        <b-col>
          <b-button @click="saveProjectHandler">Save</b-button>
        </b-col>
      </b-form-row>
    </b-form>

    <b-form class="mt-4">
      <b-file @change="fileHandler" multiple></b-file>
    </b-form>

    <div>
      {{ filestr }}
    </div>
  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";

export default {
  name: "Project",
  data() {
    return {
      filestr: "",
      local_project: {
        name: null,
        configuration: null,
        data: null,
      }
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.id
    },
  },
  methods: {
    ...mapActions(["updateProject"]),
    saveProjectHandler() {
      this.updateProject(this.local_project)
    },
    fileHandler(e) {
      const self = this
      const fileList = e.target.files
      for (let file of fileList) {
        const reader = new FileReader()
        reader.onload = function (e) {
          console.log(e.target.result)
          self.filestr += e.target.result

        }
        reader.readAsText(file)
      }

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
    }
  }
}
</script>

<style scoped>

</style>
