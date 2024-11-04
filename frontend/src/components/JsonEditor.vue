<template>
  <VJsoneditor v-model="inputVal" :options="jeOptions" :plus="false" height="800px"></VJsoneditor>
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
                "enum": ["text", "textarea", "selector", "checkbox", "radio", "html"]
              },
              "title": {"type": "string"},
              "description": {"type": "string"},
              "optional": {"type": "boolean"},
              "valSuccess": {"type": "string"},
              "valError": {"type": "string"},
              "if": {"type": "string"}
            },
            "allOf": [
              {
                // html type should have the field text
                "if": {
                  "properties": {
                    "type": {
                      "anyOf": [
                        {"const": "html"},
                      ]
                    }
                  }
                },
                "then": {
                  "properties": {
                    "text": {"type": "string"}
                  },
                  "required": ["text"]
                }
              },
              {
                // text and textarea can have the fields regex for checking
                "if": {
                  "properties": {
                    "type": {
                      "anyOf": [
                        {"const": "text"},
                        {"const": "textarea"}
                      ]
                    }
                  }
                },
                "then": {
                  "properties": {
                    "regex": {"type": "string"}
                  },
                }
              },
              {
                // selector, checkbox and radio should have the options field with at least
                // one item
                "if": {
                  "properties": {
                    "type": {
                      "anyOf": [
                        {"const": "selector"},
                        {"const": "checkbox"},
                        {"const": "radio"}
                      ]
                    }
                  }
                },
                "then": {
                  "properties": {
                    "options": {
                      "oneOf": [
                        {
                          "type": "array",
                          "minItems": 1,
                          "uniqueItems": true,
                          "items": {
                            "oneOf": [
                              {
                                "type:": "object",
                                "properties": {
                                  "label": {"type": "string"},
                                  "htmlLabel": {"type": "string"},
                                  "value": {
                                    "anyOf": [
                                      {"type": "string"},
                                      {"type": "integer"},
                                      {"type": "number"}
                                    ]
                                  }
                                },
                                "oneOf":[
                                  {"required": ["label", "value"]},
                                  {"required": ["htmlLabel", "value"]}
                                ]
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "fromDocument": {"type": "string"},
                                  "separator": {"type": "string"},
                                  "valueLabelSeparator": {"type": "string"}
                                },
                                "required": ["fromDocument"]
                              }
                            ]
                          }
                        },
                        {
                          "type": "object",
                          "minProperties": 1,
                          "additionalProperties": {"type": "string"}
                        }
                      ]
                    }
                  },
                  "required": ["options"]
                }
              },
              {
                // checkbox and radio may have "orientation" of "vertical" or "horizontal"
                "if": {
                  "properties": {
                    "type": {
                      "anyOf": [
                        {"const": "checkbox"},
                        {"const": "radio"}
                      ]
                    }
                  }
                },
                "then": {
                  "properties": {
                    "orientation": {
                      "enum": ["vertical", "horizontal"]
                    }
                  }
                }
              }
            ],
            "required": ["name", "type"],
            "unevaluatedProperties": false
          },
          "minItems": 1
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
