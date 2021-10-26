<template>

  <b-tabs>
    <b-tab title="Editor">
      <b-textarea v-model="content" rows="5" max-rows="20"></b-textarea>
    </b-tab>
    <b-tab title="Preview">
      <MarkdownRenderer :content="content" style="min-height: 10rem"></MarkdownRenderer>
    </b-tab>
  </b-tabs>
</template>

<script>
import MarkdownRenderer from "@/components/MarkdownRenderer";
export default {
  name: "MarkdownEditor",
  components: {MarkdownRenderer},
  props: {
    value: {
      default: ""
    }
  },
  computed: {
    content: {
      get(){
        return this.value
      },
      set(newValue){
        this.$emit("input", newValue)
      }
    }
  }
}
</script>

<style scoped>

</style>
