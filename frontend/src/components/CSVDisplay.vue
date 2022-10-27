<template>
  <div>
    <b-input-group>
      <b-form-file
                   placeholder="Choose a csv file or drop it here..."
                   class="mr-2"
                   accept=".csv"
                   data-cy="file-input"
                   @input="loadFileHandler"
      ></b-form-file>
    </b-input-group>
    <b-table :items="items"
             ref="csvDisplayTable"
             selectable
             select-mode="single"
             @row-selected="rowSelectionHandler"
             class="mt-4"
             per-page="10"
    >
      <template #head()="{ column }">
        {{ column }}
      </template>
    </b-table>
  </div>
</template>

<script>
const csv = require("csvtojson")
import {readFileAsync} from "@/utils";

/**
 * Component for uploading and displaying CSV file
 */
export default {
  name: "CSVDisplay",
  data() {
    return {
      items: null,
    }
  },
  props: ['value'],
  methods:{
    rowSelectionHandler(selectedRows){
      let selectedObj = {}
      if(selectedRows.length > 0){
        selectedObj = selectedRows[0]
      }
      /**
       * Row selection changed event
       */
      this.$emit("selected-row-value", selectedObj)
    },
    async loadFileHandler(file){
      if(file != null){
        const csv_str = await readFileAsync(file)
        /**
         * CSV document uploaded input event
         */
        this.$emit("input", csv_str)
        this.convertCSVStringToItems(csv_str)
      }
    },
    async convertCSVStringToItems(csv_string){
      if(csv_string != null && csv_string.length > 0)
        this.items = await csv().fromString(csv_string)

    }
  },
  watch: {
    value: {
      handler(){
        this.convertCSVStringToItems(this.value)
      }
    },
    items: {
      handler(){
        let self = this
        setTimeout(function (){
          self.$refs.csvDisplayTable.selectRow(0)

        }, 100)

      }
    }
  }
}
</script>

<style scoped>

</style>
