<template>
  <div class="projects">
      <h1>Projects</h1>
      <b-table striped hover :items="projects"></b-table>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  name: 'Projects',
  props: {},
  methods:{
    ...mapActions(["getProjects"])
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
