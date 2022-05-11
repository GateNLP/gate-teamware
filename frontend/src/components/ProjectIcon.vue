<template>
<span :title="'Project ID'+projectId" class="projectIcon rounded ml-1 mr-1">
  <b-iconstack :scale="scale" :shift-v="shiftV">
    <b-icon-clipboard></b-icon-clipboard>
    <b-icon-gear-fill scale="0.5" shift-v="-1"></b-icon-gear-fill>
  </b-iconstack>
  {{ projectId }}
</span>
</template>

<script>
export default {
  name: "ProjectIcon",
  props: {
    projectId: {
      default: 0
    },
    scale: {
      default: 0.3
    },
    shiftV: {
      default: 3
    }
  }
}
</script>

<style scoped>

.projectIcon {
  background: #0069d9;
  cursor: pointer;
  color: white !important;
  text-decoration: none !important;
  padding: 0.05rem;
}

.projectIcon:hover{
  text-decoration: none !important;
}

</style>
