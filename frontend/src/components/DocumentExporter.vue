<template>
  <b-modal title="Export documents and annotations" v-model="showModal">
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
      exportType: "json",
      jsonExportFormat: "raw",
      rawJsonExportDescription: "Export as JSON in the same format that's uploaded. Additional field named 'annotation_sets' is added for storing annotations. If you've originally uploaded in GATE format then choose this option.",
      gateJsonExportDescription: "Convert documents to GATE JSON format and export. A 'name' field is added that takes the ID value from the ID field specified in te project config. Fields apart from 'text' and the ID field specified in the project config are placed in the 'features' field. An 'annotation_sets' field is added for storing annotations."

    }
  },
  props: {
    value:{
      default: false
    },
    projectId: {
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
      }

      return false
    }
  },
  methods: {
    async exportDocumentsHandler() {
      if(this.isExportConfigValid){
        window.location.href = `/download_annotations/${this.projectId}/${this.exportType}/${this.jsonExportFormat}/500/`
      }
    },
  }
}
</script>

<style scoped>

</style>