<template>
  <b-modal title="Export documents and annotations" v-model="showModal">
    <b-form-group label="Document type">
      <b-form-radio-group v-model="documentType">
        <b-form-radio value="all">All</b-form-radio>
        <b-form-radio value="training">Training</b-form-radio>
        <b-form-radio value="test">Test</b-form-radio>
        <b-form-radio value="annotation">Annotate</b-form-radio>

      </b-form-radio-group>
    </b-form-group>
    <b-form-group label="Export type">
      <b-form-radio-group v-model="exportType">
        <b-form-radio value="json">JSON</b-form-radio>
        <b-form-radio value="jsonl">JSONL</b-form-radio>
        <b-form-radio value="csv">CSV</b-form-radio>
      </b-form-radio-group>
    </b-form-group>
    <b-form-group v-if="exportType === 'json' || exportType === 'jsonl'"
                  label="JSON Export format"
                  :description="jsonExportFormatDescription">
      <b-form-radio-group v-model="jsonExportFormat">
        <b-form-radio value="raw">Raw</b-form-radio>
        <b-form-radio value="gate">GATE</b-form-radio>
      </b-form-radio-group>
    </b-form-group>
    <b-form-group label="Anonymize Annotators"
                  :description="anonymizeAnnotatorsDescription">
      <b-form-radio-group v-model="anonymizeAnnotators">
        <b-form-radio value="anonymize">Yes</b-form-radio>
        <b-form-radio value="deanonymize">No</b-form-radio>
      </b-form-radio-group>
    </b-form-group>
    <template v-slot:modal-footer>
      <div style="display: flex">
        <b-button class="mr-2" @click="showModal = false">Close</b-button>
        <b-button variant="primary" @click="exportDocumentsHandler" :disabled="!isExportConfigValid">Export</b-button>
      </div>
    </template>
  </b-modal>

</template>

<script>
import {toastError} from "@/utils";

export default {
  name: "DocumentExporter",
  data(){
    return {
      documentType: "all",
      exportType: "json",
      jsonExportFormat: "raw",
      anonymizeAnnotators: "anonymize",
      rawJsonExportDescription: "Export as JSON in the same format that's uploaded. Additional field named 'annotation_sets' is added for storing annotations. If you've originally uploaded in GATE format then choose this option.",
      gateJsonExportDescription: "Convert documents to GATE JSON format and export. A 'name' field is added that takes the ID value from the ID field specified in te project config. Fields apart from 'text' and the ID field specified in the project config are placed in the 'features' field. An 'annotation_sets' field is added for storing annotations.",
      anonymizeAnnotatorsDescription: "Anonymizing annotators exports anonymous user IDs in place of usernames."
    }
  },
  props: {
    value:{
      default: false
    },
    projectId: {
    },
    defaultDocType: {
      default: "all"
    }
  },
  computed: {
    showModal: {
      get(){
        return this.value;
      },
      set(newValue){
        this.$emit('input', newValue)
      }
    },
    jsonExportFormatDescription(){
      if(this.jsonExportFormat === "raw"){
        return this.rawJsonExportDescription
      }
      else if(this.jsonExportFormat === "gate"){
        return this.gateJsonExportDescription
      }
      else{
        return ""
      }
    },
    isExportConfigValid(){
      let exportType = this.exportType
      let jsonExportFormat = this.jsonExportFormat
      if(exportType){
        if(exportType === "csv"){
          return true
        }

        if( (exportType === "json" || exportType === "jsonl") &&
            (jsonExportFormat === "raw" || jsonExportFormat === "gate" )
        ){
          return true
        }

        if( (anonymizeAnnotators === true || anonymizeAnnotators === false ) ){
          return true
        }
      }

      return false
    }
  },
  methods: {
    async exportDocumentsHandler() {
      if(this.isExportConfigValid){
        window.location.href = `/download_annotations/${this.projectId}/${this.documentType}/${this.exportType}/${this.jsonExportFormat}/500/${this.anonymizeAnnotators}/`
      }
    },
  },
  watch: {
    defaultDocType: {
      immediate: true,
      handler(newValue){
        this.documentType = newValue
      }
    }
  }
}
</script>

<style scoped>

</style>
