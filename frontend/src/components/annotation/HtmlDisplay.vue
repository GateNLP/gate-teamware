<template>
  <div v-html="htmlDisplay"></div>
</template>

<script>
import Mustache from "mustache"

export default {
  name: "HtmlDisplay",
  props: ["config", "document"],
  computed: {
    htmlDisplay() {

      try {
        if (this.config && this.config.text) {
          let context = {}
          if (this.document) {
            context = this.document
          }

          let output = Mustache.render(this.config.text, context)
          return output
        }

      } catch (e) {
        console.log(e)
      }


      return ""

    }
  }
}
</script>

<style scoped>

</style>
