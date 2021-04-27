<template>
  <div class="projects">
      <h2>Projects</h2>
      <b-table striped hover :items="items"></b-table>
  </div>
</template>

<script>
export default {
  name: 'ProjectList',
  props: {},
  data() {
      return {
        items: [
          { id: 40, name: 'test project'},
          { id: 21, name: 'test project'},
          { id: 89, name: 'test project'},
          { id: 38, name: 'test project' }
        ]
      }
    },
}
</script>

<style scoped>
</style>
