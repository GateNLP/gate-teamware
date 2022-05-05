<template>
  <div class="annotation">
    <div v-for="elemConfig in config" :key="elemConfig.name">
      <b-card class="mb-4" v-if="(elemConfig.type != 'html') && (document_type == DocumentType.Training)">
        <MarkdownRenderer :content="document[doc_gold_field][elemConfig.name].explanation"></MarkdownRenderer>
      </b-card>
      <b-form-group :label="elemConfig.title">
        <p class="annotation-description" v-if="elemConfig.description">{{ elemConfig.description }}</p>
        <component v-if="getInputType(elemConfig.type)"
                   :is="getInputType(elemConfig.type)"
                   :name="elemConfig.name"
                   :config="elemConfig"
                   :document="document"
                   v-model="annotationOutput[elemConfig.name]"
                   :state="validation[elemConfig.name]"
                   :msg-success="elemConfig.valSuccess"
                   :msg-error="elemConfig.valError"
                   @input="inputEventHandler"></component>
        <div v-else>
          Component invalid
        </div>
      </b-form-group>
    </div>
    <b-row>
      <b-col>
        <BButton @click.prevent="submitHandler" class="mr-4" variant="success">Submit</BButton>
        <BButton @click.prevent="clearFormHandler" class="mr-4" variant="warning">Clear</BButton>
        <BButton v-if="allow_document_reject" @click.prevent="rejectHandler" variant="danger">Reject document</BButton>
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
import {DocumentType} from '@/enum/DocumentTypes';
import MarkdownRenderer from "@/components/MarkdownRenderer";

/**
 * Renders annotation display and input capture from the config property
 */
export default {
  name: "AnnotationRenderer",
  components: {TextInput, TextareaInput, RadioInput, CheckboxInput, SelectorInput, HtmlDisplay, MarkdownRenderer},
  data() {
    return {
      annotationOutput: {},
      validation: {},
      validationErrorMsg: {},
      inputTypes: {
        text: 'TextInput',
        textarea: 'TextareaInput',
        radio: 'RadioInput',
        checkbox: 'CheckboxInput',
        selector: 'SelectorInput',
        html: 'HtmlDisplay',
      },
      ignoreValidateTypes: ['html'],
      startTime: null,
      DocumentType
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
      },
    },
    document_type: {
      default: null
    },
    doc_gold_field: {
      default: 'gold'
    },
    allow_document_reject: {
      default: null
    }
  },
  methods: {
    startTimer(){
      this.startTime = new Date();
    },
    getTimeElapsed(){
      if (this.document_type != this.DocumentType.Annotation){
        return null
      }
      let endTime = new Date();
      return (endTime - this.startTime)/1E3;
    },
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

      this.validation = {}
      this.validationErrorMsg = {}


      for (let elemConfig of this.config) {

        const elemName = elemConfig.name
        const elemType = elemConfig.type

        if (!this.ignoreValidateTypes.includes(elemType) && 
            (!elemConfig.optional || (elemType === "checkbox" && "minSelected" in elemConfig))) {
          // Validate to false as default
          this.validation[elemName] = false

          // Entry exists
          if (elemName in this.annotationOutput && this.valueNotEmpty(this.annotationOutput[elemName])) {

            if ((elemType === "text" || elemType === "textarea") && "regex" in elemConfig) {
              const regex = new RegExp(elemConfig.regex)
              this.validation[elemName] = regex.test(this.annotationOutput[elemName])

            } else if (elemType === "checkbox" && "minSelected" in elemConfig) {
              this.validation[elemName] = elemConfig.minSelected <= this.annotationOutput[elemName].length

            } else {
              this.validation[elemName] = true
            }

          }
        } else {
          //Remove the validation key if validation is not needed
          if (elemConfig.name in this.validation) {
            delete this.validation[elemName]
          }
        }
      }

      let validationPassed = true
      for (let key in this.validation) {
        if (!this.ignoreValidateTypes.includes(key) && !this.validation[key]) {
          validationPassed = false
        }
      }

      return validationPassed
    },
    valueNotEmpty(val) {
        if (typeof val === 'string' && val.length > 0) {
          return true
        }

        if (val instanceof Array && val.length > 0) {
          return true
        }

        return false
    },
    submitHandler(e) {
      let elapsedTime = this.getTimeElapsed();
      let validationPassed = this.validateAnnotation()
      this.$forceUpdate()

      if (validationPassed) {
        this.$emit('submit', this.annotationOutput, elapsedTime)
        this.clearForm()
        this.startTimer();
      }
    },
    clearForm() {
      this.annotationOutput = {}
      this.validation = {}

    },
    clearFormHandler(e) {
      this.clearForm()
    },
    rejectHandler(e){
      this.$emit('reject')
      this.startTimer();
    }
  },
  watch: {
    config: {
      immediate: true,
      handler(newConfig) {
        this.generateValidationTracker(newConfig)
      }
    }
  },
  mounted(){
    this.startTimer();
  }

}
</script>

<style scoped>

</style>
