<template>
  <div class="projects container">
    <h1>Projects</h1>

    <b-button-toolbar class="mb-4">
      <b-button @click="handleCreateProject" variant="primary">Create project</b-button>
    </b-button-toolbar>

    <Search @input="searchProject"></Search>

    <Pagination class="mt-4" :items="filteredProjects" v-slot:default="{ pageItems }">
      <b-list-group class="mb-4">
        <b-list-group-item v-for="project in pageItems" :key="project.id">
          <div class="d-flex justify-content-between">
            <div>
              <b-link :to="'/project/'+project.id">{{ project.name }}</b-link>

            </div>
            <div>
              <b-badge variant="success" class="mr-2" title="Completed annotations">
                <b-icon-pencil-fill></b-icon-pencil-fill>
                {{ project.completed_tasks }}
              </b-badge>
              <b-badge variant="danger" class="mr-2" title="Rejected annotations">
                <b-icon-x-square-fill></b-icon-x-square-fill>
                {{ project.rejected_tasks }}
              </b-badge>
              <b-badge variant="warning" class="mr-2" title="Timed out annotations">
                <b-icon-clock></b-icon-clock>
                {{ project.timed_out_tasks }}
              </b-badge>
              <b-badge variant="secondary" class="mr-2" title="Aborted annotations">
                <b-icon-stop-fill></b-icon-stop-fill>
                {{ project.aborted_tasks }}
              </b-badge>
              <b-badge variant="primary" class="mr-2" title="Pending annotations">
                <b-icon-play-fill></b-icon-play-fill>
                {{ project.pending_tasks }}
              </b-badge>
              <b-badge variant="dark" class="mr-2" title="Occupied (completed & pending)/Total tasks">
                <b-icon-card-checklist></b-icon-card-checklist>
                {{ project.completed_tasks + project.pending_tasks }}/{{ project.total_tasks }}
              </b-badge>
              <b-badge variant="info" class="mr-2" title="Number of documents">
                <b-icon-file-earmark-fill></b-icon-file-earmark-fill>
                {{ project.documents }}
              </b-badge>

            </div>

          </div>

          <div>
            <b-icon-person-fill></b-icon-person-fill>
            Created by: {{ project.owned_by }}
          </div>

          <div>
            <b-icon-clock class="mr-2"></b-icon-clock>
            Created: {{ project.created | datetime }}
          </div>

        </b-list-group-item>
      </b-list-group>
    </Pagination>



  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex'
import Pagination from "@/components/Pagination";
import Search from "@/components/Search";
import _ from "lodash"
import {toastError} from "@/utils";

export default {
  name: 'Projects',
  title: "Projects",
  components: {Search, Pagination},
  data(){
    return {
      searchStr: null,
      projects: [],
    }
  },
  props: {},
  methods: {
    ...mapActions(["getProjects", "createProject"]),
    async updateProjectList(){
      try{
        this.projects = await this.getProjects();
      }catch (e){
        toastError(this, "Could not fetch project list", e)
      }

    },
    async handleCreateProject() {
      if (this.user && this.user.isAuthenticated) {
        let projectObj = await this.createProject()
        this.$router.push("/project/" + projectObj.id)
      }
    },
    searchProject(searchStr){
      this.searchStr = searchStr
    }
  },
  computed: {
    ...mapState(["user"]),
    filteredProjects(){
      if(!this.searchStr || this.searchStr.trim().length < 1)
        return this.projects

      let searchStr = this.searchStr

      // Currently searching for project names only
      let result = _.filter(
          this.projects,
          function (o){ return _.includes(_.lowerCase(o.name), _.lowerCase(searchStr)) }
          )
      return result

    }
  },
  mounted() {
    this.updateProjectList()
  }
}
</script>

<style scoped>
</style>
