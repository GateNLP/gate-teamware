<template>
  <div>
    <VJsoneditor v-model="inputVal" :options="jeOptions" :plus="false" height="800px"></VJsoneditor>

  </div>

</template>

<script>
import VJsoneditor from "v-jsoneditor"


export default {
  name: "JsonEditor",
  components: {VJsoneditor},
  data() {
    return {
      jeOptions: {
        mode: "code",
        schema: {
          // "$schema": "https://json-schema.org/draft/2020-12/schema",
          "$id": "https://example.com/product.schema.json",
          "title": "Project config schema",
          "description": "Declares valid object types",
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "type": {
                "type": "string"
              }
            },
            "required": ["name", "type"]
          }
        },

      },
    }
  },
  props: {
    value: {
      default: null
    },
  },
  computed: {
    inputVal: {
      set(val) {
        this.$emit('input', val)
      },
      get() {
        return this.value
      }
    },
  },
  methods: {
    onValidationError(e) {
      console.log("Validation error")
      console.log(e)
    }

  },
  watch: {}
}
</script>

<style scoped>

</style>
