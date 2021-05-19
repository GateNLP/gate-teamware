<template>
  <div>
    <div v-for="elemConfig in config" :key="elemConfig.name">
      <b-form-group :label="elemConfig.title">
        <p v-if="elemConfig.description">{{ elemConfig.description }}</p>
        <component v-if="getInputType(elemConfig.type)"
                   :is="getInputType(elemConfig.type)"
                   :name="elemConfig.name"
                   :config="elemConfig"
                   :document="document"
                   v-model="annotationOutput[elemConfig.name]"
                   :state="validation[elemConfig.name]"
                   @input="inputEventHandler"></component>
      </b-form-group>
    </div>
    <BButton @click.prevent="submitHandler">Submit</BButton>
  </div>
</template>

<script>

import TextInput from "@/components/annotation/TextInput";
import TextareaInput from "@/components/annotation/TextareaInput";
import RadioInput from "@/components/annotation/RadioInput";
import CheckboxInput from "@/components/annotation/CheckboxInput";
import SelectorInput from "@/components/annotation/SelectorInput";
import HtmlDisplay from "@/components/annotation/HtmlDisplay";

export default {
  name: "AnnotationRenderer",
  components: {TextInput, TextareaInput, RadioInput, CheckboxInput, SelectorInput, HtmlDisplay},
  data() {
    return {
      annotationOutput: {},
      validation: {},
      inputTypes: {
        text: 'TextInput',
        textarea: 'TextareaInput',
        radio: 'RadioInput',
        checkbox: 'CheckboxInput',
        selector: 'SelectorInput',
        html: 'HtmlDisplay',
      },
      ignoreValidateTypes: ['html'],
    }
  },
  props: {
    config: {
      default: null
    },
    document: {
      default() {
        return {
          text: "<p>Some html text <strong>in bold</strong>.</p><p>Paragraph 2.</p>"
        }
      }
    }
  },
  methods: {
    inputEventHandler(e) {
      this.$emit('input', this.annotationOutput)
    },
    getInputType(name) {
      if (name in this.inputTypes) {
        return this.inputTypes[name]
      }

      return null
    },
    generateValidationTracker(config) {
      if (config) {
        this.validation = {}
        for (let elemConfig of config) {
          this.validation[elemConfig.name] = null
        }
      }
    },
    validateAnnotation() {
      for (let elemConfig of this.config) {
        if (!this.ignoreValidateTypes.includes(elemConfig.type)) {
          if (elemConfig.name in this.annotationOutput) {
            this.validation[elemConfig.name] = true
          } else {
            this.validation[elemConfig.name] = false
          }
        }
      }

      let validationPassed = true
      for(let key in this.validation){
        if(!this.ignoreValidateTypes.includes(key) && !this.validation[key]){
          validationPassed = false
        }
      }

      return validationPassed
    },
    submitHandler(e) {
      let validationPassed = this.validateAnnotation()
      this.$forceUpdate()

      if(validationPassed){
        this.$emit('submit', this.annotationOutput)
      }
    }

  },
  watch: {
    config: {
      immediate: true,
      handler(newConfig) {
        this.generateValidationTracker(newConfig)
      }
    }
  }

}
</script>

<style scoped>

</style>
