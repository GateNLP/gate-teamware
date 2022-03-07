<template>
  <div class="projects container">
    <h1>Projects</h1>

    <b-button-toolbar class="mb-4">
      <b-button @click="handleCreateProject" variant="primary">Create project</b-button>
    </b-button-toolbar>

    <Search @input="searchProject"></Search>

    <PaginationAsync class="mt-4"
                     :items="projects"
                     :num-items="numTotalProjects"
                     :items-per-page="itemsPerPage"
                     :is-loading="loading"
                     v-model="currentPage"
                     @page-size-change="handleItemPerPageChange"
                     v-slot:default="{ pageItems }">
      <b-list-group class="mb-4">
        <b-list-group-item v-for="project in pageItems" :key="project.id" data-role="project_container">
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
    </PaginationAsync>
  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex'
import Pagination from "@/components/Pagination";
import PaginationAsync from "@/components/PaginationAsync";
import Search from "@/components/Search";
import _ from "lodash"
import {toastError} from "@/utils";
import ProjectIcon from "@/components/ProjectIcon";
import ProjectStatusBadges from "@/components/ProjectStatusBadges";

export default {
  name: 'Projects',
  title: "Projects",
  components: {ProjectStatusBadges, ProjectIcon, Search, Pagination, PaginationAsync},
  data(){
    return {
      searchStr: null,
      currentPage: 1,
      itemsPerPage: 10,
      numTotalProjects: 0,
      projects: [],
      loading: false,
    }
  },
  props: {},
  methods: {
    ...mapActions(["getProjects", "createProject"]),
    async fetchProjectItems(){

      try{
        this.setLoading(true)
        const result = await this.getProjects({
          current_page: this.currentPage,
          page_size: this.itemsPerPage,
          filters: this.searchStr,
        })

        this.projects = result.items
        this.numTotalProjects = result.total_count

      }catch(e){
        toastError("Could not fetch projects list", e)
      }finally {
        this.setLoading(false)
      }

    },
    searchProject(searchStr){
      this.searchStr = searchStr
      this.fetchProjectItems()
    },
    handleItemPerPageChange(newValue){
      this.itemsPerPage = newValue
      this.fetchProjectItems()
    },
    async handleCreateProject() {
      if (this.user && this.user.isAuthenticated) {
        let projectObj = await this.createProject()
        this.$router.push("/project/" + projectObj.id)
      }
    },
    async setLoading(isLoading){
      this.loading = isLoading
    }
  },
  computed: {
    ...mapState(["user"]),
  },
  watch:{
    currentPage: {
      handler(){
        this.fetchProjectItems()
      }
    }
  },
  mounted() {
    this.fetchProjectItems()
  }
}
</script>

<style scoped>
</style>
