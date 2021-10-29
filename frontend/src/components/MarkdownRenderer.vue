<template>
  <markdown-it-vue :content="content" :options="options" ></markdown-it-vue>
</template>

<script>
export default {
name: "MarkdownRenderer",
  props: {
    content: {
      default: ""
    },
    options: {
      default(){
        return {markdownIt: { html: true } }
      }
    },

  }
}
</script>

<style scoped>

</style>
