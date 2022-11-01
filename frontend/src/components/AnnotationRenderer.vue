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
                   :msg-success="elemConfig.valSuccess"
                   :msg-error="elemConfig.valError"
                   @input="inputEventHandler"></component>
        <div v-else>
          Component invalid
        </div>
        <b-card class="mb-4"
          :border-variant="answerBgColor[elemConfig.name]"
          v-if="showExplanation(elemConfig)">
          <MarkdownRenderer :content="answerText(elemConfig) + '<br>' + document[doc_gold_field][elemConfig.name].explanation"></MarkdownRenderer>
        </b-card>
      </b-form-group>
    </div>
    <b-row>
      <b-col>
        <BButton @click.prevent="submitHandler" class="mr-4" variant="success">Submit</BButton>
        <BButton @click.prevent="clearFormHandler" class="mr-4" variant="warning">Clear</BButton>
        <BButton v-if="allow_document_reject" @click.prevent="rejectHandler" variant="danger">Reject document</BButton>
        <BButton v-if="allow_cancel" @click.prevent="cancelHandler" variant="danger">Cancel</BButton>
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
import {getValueFromKeyPath} from "@/utils";
import _ from "lodash"

/**
 * Renders annotation display and input capture from the config property
 *
 * Events
 * submit(annotationOutput, elapsedTime) - When user presses the submit button
 * reject() - When user presses the reject button
 * cancel() - When user presses the cancel button
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
      DocumentType,
      answerBgColor: {}
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
    /**
     * This field will be used to provide pre-annotation
     * i.e. pre-filling the form before it's presented to the user
     */
    doc_preannotation_field: {
      default: ""
    },
    /**
     * Adds Reject button if true
     */
    allow_document_reject: {
      default: null
    },
    /**
     * Adds a Cancel button if true
     */
    allow_cancel: {
      default: null
    },
    clear_after_submit: {
      default: true,
      type: Boolean
    }
  },
  computed: {
    preAnnotationValues(){
      if(this.document != null && this.doc_preannotation_field != null){
        return  getValueFromKeyPath(this.document, this.doc_preannotation_field)
      }
      return null
    }

  },
  methods: {
    setAnnotationData(data){
      this.annotationOutput = data
    },
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
        if(this.clear_after_submit)
          this.clearForm()
        this.startTimer();
      }
    },
    clearForm() {
      this.annotationOutput = {}
      this.validation = {}
      this.fillWithPreAnnotation()

    },
    clearFormHandler(e) {
      this.clearForm()
    },
    rejectHandler(e){
      this.$emit('reject')
      this.startTimer();
    },
    cancelHandler(e){
      this.$emit('cancel')
      this.startTimer();
    },
    getAnswerBgColor(elemConfig){
      let answer = this.annotationOutput[elemConfig.name];
      let expected = this.document[this.doc_gold_field][elemConfig.name].value;

      if (Object.keys(elemConfig.options).includes(answer)) {
        if (answer == expected){
          return "success"
        } else {
          return "danger"
        }
      } else {
        return "Default"
      }
    },
    showExplanation(elemConfig){

      if (elemConfig.type == 'html'){
        return false
      } else if ((this.document_type == DocumentType.Training) && (Object.keys(elemConfig.options).includes(this.annotationOutput[elemConfig.name]))) {
        return true
      } else {
        return false
      }
    },
    answerText(elemConfig){
      let answer = this.annotationOutput[elemConfig.name];
      let expected = this.document[this.doc_gold_field][elemConfig.name].value;

      if (Object.keys(elemConfig.options).includes(answer)) {
        if (answer == expected){
          return "Correct! ✔️"
        } else {
          return "Incorrect ❌"
        }
      } else {
        return ""
      }
    },
    fillWithPreAnnotation(){
      if(this.preAnnotationValues != null){
          this.setAnnotationData(_.cloneDeep(this.preAnnotationValues))
        }
    }
  },
  watch: {
    config: {
      immediate: true,
      handler(newConfig) {
        this.generateValidationTracker(newConfig)
      }
    },
    document: {
      handler(){
        this.fillWithPreAnnotation()
      }
    },
    doc_preannotation_field: {
      handler(){
        this.fillWithPreAnnotation()
      }
    },
    annotationOutput: {
      immediate: true,
      deep: true,
      handler() {
        for (const prop in this.config){
          if (this.showExplanation(this.config[prop])) {
            this.answerBgColor[this.config[prop].name] = this.getAnswerBgColor(this.config[prop]);
          }
        }
      }
    }
  },
  mounted(){
    for (const prop in this.config){
      if(this.config[prop].type != 'html') {
        this.answerBgColor[this.config[prop].name] = "Default";
      }
    }
    this.startTimer();
  }

}
</script>

<style scoped>

</style>
