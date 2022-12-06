<template>
  <div class="container">
    <b-row class="my-3">
      <b-col>
        <h1 class="mb-4">My annotations</h1>

        <div v-if="annotation_projects && annotation_projects.length > 0">
          <b-row>
            <b-col md="4">
              <b-list-group>
                <b-list-group-item v-for="project in annotation_projects" button
                                   @click="currentProject = project"
                                   :key="project.id"
                                   :active="currentProject && currentProject.id == project.id">
                  {{project.name}}
                </b-list-group-item>
              </b-list-group>

            </b-col>
            <b-col md="8">
              <div v-if="currentProject">
                <UserAnnotatedProject :project="currentProject"></UserAnnotatedProject>
              </div>
              <div v-else>
                No project selected
              </div>
            </b-col>
          </b-row>
          <div >

          </div>
        </div>
        <div v-else>
          No annotations yet
        </div>

      </b-col>
    </b-row>

  </div>

</template>

<script>
import UserAnnotatedProject from "@/components/UserAnnotatedProject";
import ProjectIcon from "@/components/ProjectIcon";
import {mapActions} from "vuex";

export default {
  name: "UserAnnotations",
  title: "My Annotations",
  components: {UserAnnotatedProject, ProjectIcon},
  data(){
    return {
      annotation_projects: [],
      currentProject: null,
    }
  },
  methods: {
    ...mapActions(["getUserAnnotatedProjects"]),
  },
  async mounted() {
    this.annotation_projects = await this.getUserAnnotatedProjects();
  },
}
</script>

<style scoped>

</style>
