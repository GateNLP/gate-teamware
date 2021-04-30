<template>
  <div class="projects container">
      <h1>Projects</h1>

      <ul>
        <li v-for="project in projects" :key="project.id">
          <b-link :to="'/project/'+project.id">{{project.name}}</b-link>
        </li>
      </ul>


    <b-button @click="handleCreateProject">Create project</b-button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  name: 'Projects',
  props: {},
  methods:{
    ...mapActions(["getProjects", "createProject"]),
    async handleCreateProject(){
      let projectObj = await this.createProject()
      this.$router.push("/project/"+projectObj.id)

    }
  },
  computed:{
    ...mapState(["projects"])
  },
  beforeMount(){
    this.getProjects();
  }
}
</script>

<style scoped>
</style>
