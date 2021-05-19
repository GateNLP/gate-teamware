<template>
 <div v-html="htmlDisplay"></div>
</template>

<script>
let Mustache = require('mustache')

export default {
  name: "HtmlDisplay",
  props: ["config", "document"],
  computed: {
    htmlDisplay(){
      let context = {}
      if(this.document)
        context = this.document
      let output = Mustache.render(this.config.text, context)
      return output
    }
  }
}
</script>

<style scoped>

</style>
