<template>
  <div class="annotation">
    <div v-for="elemConfig in config" :key="elemConfig.name">
      <b-form-group :label="elemConfig.title">
        <p class="annotation-description" v-if="elemConfig.description">{{ elemConfig.description }}</p>
        <component v-if="getInputType(elemConfig.type)"
                   :is="getInputType(elemConfig.type)"
                   :name="elemConfig.name"
                   :config="elemConfig"
                   :document="document"
                   v-model="annotationOutput[elemConfig.name]"
                   :state="validation[elemConfig.name]"
                   @input="inputEventHandler"></component>
        <div v-else>
          Component invalid
        </div>
      </b-form-group>
    </div>
    <b-row>
      <b-col>
        <BButton @click.prevent="submitHandler" class="mr-4" variant="success">Submit</BButton>
        <BButton @click.prevent="clearFormHandler" variant="danger">Clear</BButton>
      </b-col>
    </b-row>
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
        if (!this.ignoreValidateTypes.includes(elemConfig.type) && !elemConfig.optional) {
          if (elemConfig.name in this.annotationOutput) {
            this.validation[elemConfig.name] = true
          } else {
            this.validation[elemConfig.name] = false
          }
        }
        else{
          //Remove the validation key if validation is not needed
          if(elemConfig.name in this.validation){
            delete this.validation[elemConfig.name]
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
        this.clearForm()
      }


    },
    clearForm(){
      this.annotationOutput = {}
      this.validation = {}

    },
    clearFormHandler(e){
      this.clearForm()
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
