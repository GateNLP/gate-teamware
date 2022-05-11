<template>
  <div>
    {{ fileStat.name }}
    <b-badge v-if="fileStat.numDocs > 0"
             :title="fileStat.uploadedDocs + ' of ' + fileStat.numDocs + ' documents uploaded'"
             :class="{
                     'badge-success': fileStat.numDocs <= fileStat.uploadedDocs
                   }"
             variant="primary"
    >
      <b-icon-file-earmark-text></b-icon-file-earmark-text>
      {{ fileStat.uploadedDocs }}
      /
      {{ fileStat.numDocs }}
    </b-badge>
    <b-badge v-else-if="fileStat.filesList.length < 1">
      Not uploaded
    </b-badge>

    <ul v-if="fileStat.filesList.length > 0">
      <li v-for="innerFileStat in fileStat.filesList">
        <DocumentUploaderItem :file-stat="innerFileStat"></DocumentUploaderItem>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "DocumentUploaderItem",
  props: {
    fileStat: {}
  }
}
</script>

<style scoped>

</style>
