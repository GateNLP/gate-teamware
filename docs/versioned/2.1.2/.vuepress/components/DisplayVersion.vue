<template>
<span>{{version_name}}</span>
</template>

<script>
import versionData from "../versions.json"
export default {
  name: "DisplayVersion",
  computed: {
    version_name(){
      return versionData.current
    }
  }


}
</script>

<style scoped>

</style>
