<template>
<div style="font-weight: bold !important;">
  <b-select :options="versionOptions" v-model="currentVersion" @change="versionChangeHandler">
  </b-select>
</div>
</template>

<script>
import versionData from "../../versions.json"
export default {
  name: "VersionSelector",
  data(){
    return {
      currentVersion: versionData.base
    }
  },
  computed: {
    versionOptions(){
      return versionData.versions
    }

  },
  methods: {
    versionChangeHandler(val){
      document.location.href = val
    }
  }
}
</script>

<style scoped>

</style>
