<template>
  <b-modal v-model="modalShow" title="Upload documents">
    <b-input-group>
      <b-form-file v-model="selectedFiles"
                   multiple placeholder="Choose a file or drop it here..."
                   class="mr-2"
                   accept=".json,.jsonl,.csv,.zip"
                   data-cy="file-input"
      ></b-form-file>
    </b-input-group>

    <div v-if="selectedFilesStats.length > 0" class="mt-2">
      <span style="font-weight: bold">Upload status</span>
      <ul>
        <li v-for="fileStat in selectedFilesStats" :key="fileStat.name">
          <DocumentUploaderItem :file-stat="fileStat"></DocumentUploaderItem>
        </li>
      </ul>
    </div>

    <template v-slot:modal-footer>
      <div style="display: flex">
        <b-button @click="modalShow = false" class="mr-2">Close</b-button>
        <b-button variant="primary" :disabled="selectedFilesStats.length < 1" @click="documentUploadHandler">Upload
      </b-button>

      </div>


    </template>
  </b-modal>
</template>

<script>
import {readFileAsync, toastError} from "@/utils";
import {mapActions} from "vuex";
import DocumentUploaderItem from "@/components/DocumentUploaderItem.vue";

import csv from "csvtojson"
import JSZip from "jszip"
import JSONL from 'jsonl-parse-stringify'
import {DocumentType} from '@/enum/DocumentTypes'

export default {
  name: "DocumentUploader",
  components: {DocumentUploaderItem},
  data() {
    return {
      selectedFiles: null,
      selectedFilesStats: [],
      DocumentType
    }
  },
  props: {
    value: {
      default: false
    },
    projectId: {},
    documentType:{
      type: String,
      default: DocumentType.Annotation
    }
  },
  computed: {
    modalShow: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      }
    },
  },
  methods: {
    ...mapActions(["addProjectDocument", "addProjectTestDocument", "addProjectTrainingDocument"]),
    async documentUploadHandler() {

      try {
        this.$emit("uploading")
        for (let fileStat of this.selectedFilesStats) {
          await this.uploadFile(fileStat)
        }

      } catch (e) {
        toastError("Could not upload document", e, this)

      }finally {
        this.$emit("completed")
      }

    },
    async uploadFile(fileStat) {
      const fileName = fileStat.name.trim().toLowerCase()
      if (fileName.endsWith(".json")) {
        await this.uploadJSONFile(fileStat)
      } else if (fileName.endsWith(".jsonl")){
        await this.uploadJSONLFile(fileStat)
      } else if (fileName.endsWith(".csv")) {
        await this.uploadCSVFile(fileStat)
      } else if (fileName.endsWith(".zip")) {
        await this.uploadZipFile(fileStat)
      }

    },
    async getFileStatStringContent(fileStat){
      let content = null
      if(fileStat.isZip){
        content = await fileStat.file.async("string")
      }
      else{
        content = await readFileAsync(fileStat.file)
      }

      return content
    },
    async uploadJSONFile(fileStat) {
      try {
        const documentsStr = await this.getFileStatStringContent(fileStat)
        const documents = JSON.parse(documentsStr)
        const numDocs = documents.length

        //Set this way to make map reactive
        this.$set(fileStat, "numDocs", numDocs)

        // Uploaded file must be an array of docs
        if (documents instanceof Array) {
          let uploadedDocs = 0
          for (let document of documents) {

            uploadedDocs += 1

            //Set this way to make map reactive
            this.$set(fileStat, "uploadedDocs", uploadedDocs)

            await this.uploadDocument(this.projectId, document)

          }
        }

      } catch (e) {
        console.error("Could not parse uploaded file")
        console.error(e)
        toastError("Could not parse uploaded file " + fileStat.name, e, this)
      }
    },
    async uploadJSONLFile(fileStat) {
      try {
        const documentsStr = await this.getFileStatStringContent(fileStat)
        const documents = JSONL.parse(documentsStr)
        const numDocs = documents.length

        //Set this way to make map reactive
        this.$set(fileStat, "numDocs", numDocs)

        // Uploaded file must be an array of docs
        if (documents instanceof Array) {
          let uploadedDocs = 0
          for (let document of documents) {

            uploadedDocs += 1

            //Set this way to make map reactive
            this.$set(fileStat, "uploadedDocs", uploadedDocs)

            await this.uploadDocument(this.projectId, document)
          }
        }

      } catch (e) {
        console.error("Could not parse uploaded file")
        console.error(e)
        toastError("Could not parse uploaded file " + fileStat.name, e, this)
      }
    },
    async uploadCSVFile(fileStat) {
      try {
        const documentsStr = await this.getFileStatStringContent(fileStat)
        const documents = await csv().fromString(documentsStr)
        const numDocs = documents.length

        //Set this way to make map reactive
        this.$set(fileStat, "numDocs", numDocs)

        // Uploaded file must be an array of docs
        if (documents instanceof Array) {
          let uploadedDocs = 0
          for (let document of documents) {

            uploadedDocs += 1

            //Set this way to make map reactive
            this.$set(fileStat, "uploadedDocs", uploadedDocs)

            await this.uploadDocument(this.projectId, document)
          }
        }


      } catch (e) {
        console.error("Could not parse uploaded file")
        console.error(e)
        toastError("Could not parse uploaded file " + fileStat.name, e, this)
      }

    },
    async uploadZipFile(fileStat) {
      try {
        let zip = new JSZip()
        let docZip = await zip.loadAsync(fileStat.file)

        let fileListing = []
        for (let fileName in docZip.files) {
          let fileProp = docZip.files[fileName]

          if (!fileProp.dir) {
            fileListing.push({
              name: fileName,
              file: fileProp,
              isZip: true,
              numDocs: 0,
              uploadedDocs: 0,
              filesList: []
            })
          }
        }
        this.$set(fileStat, "filesList", fileListing)

        for(let zippedFileStat of fileListing){
          await this.uploadFile(zippedFileStat)
        }

      } catch (e) {
        console.error("Could not parse uploaded file")
        console.error(e)
        toastError("Could not parse uploaded file " + fileStat.name, e, this)
      }

    },
    async uploadDocument(projectId, docContents){
      switch (this.documentType){
        case DocumentType.Test:
          return await this.addProjectTestDocument({projectId: projectId, document: docContents})
        case DocumentType.Training:
          return await this.addProjectTrainingDocument({projectId: projectId, document: docContents})
        default:
          return await this.addProjectDocument({projectId: projectId, document: docContents})

      }

    }
  },
  watch: {
    selectedFiles: {
      handler() {

        let statsArray = []
        if (this.selectedFiles) {
          for (let file of this.selectedFiles) {
            statsArray.push({
              name: file.name,
              file: file,
              numDocs: 0,
              uploadedDocs: 0,
              filesList: []
            })
          }
        }

        this.selectedFilesStats = statsArray
      }
    }
  }
}
</script>

<style scoped>

</style>
