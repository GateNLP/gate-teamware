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

              <b-link :to="'/project/'+project.id">
                <ProjectIcon :project-id="project.id" scale="1" shift-v="0"></ProjectIcon>
                {{ project.name }}
              </b-link>
              <b-badge variant="warning" v-if="!project.is_configured" :title="project.configuration_error.join(', ')" class="ml-2"><b-icon-exclamation-triangle></b-icon-exclamation-triangle></b-badge>
              <b-badge variant="success" v-else-if="project.is_completed" title="All annotation tasks in the project are completed." class="ml-2"><b-icon-check-square></b-icon-check-square></b-badge>
            </div>
            <ProjectStatusBadges :project="project"></ProjectStatusBadges>

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
import ProjectIcon from "@/components/ProjectIcon";
import ProjectStatusBadges from "@/components/ProjectStatusBadges";

export default {
  name: 'Projects',
  title: "Projects",
  components: {ProjectStatusBadges, ProjectIcon, Search, Pagination},
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
