<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">

    <b-form-checkbox-group 
      v-model="inputVal"
      :stacked="config.orientation=='vertical'"
      >
      
      <b-form-checkbox 
        :key="option.value" 
        :value="option.value" 
        :state="state"
        v-for="option in options"
        :name="config.name"
        >
        {{ option.text }}
        <b-icon-question-circle v-if="option.helptext != null" :id="option.value" class="annotation-help-prompt"></b-icon-question-circle>
        <b-tooltip v-if="option.helptext != null" :target="option.value" :title="option.helptext"></b-tooltip>
      </b-form-checkbox>

    </b-form-checkbox-group>
  </InputErrorDisplay>
</template>

<script>
import { generateBVOptions } from '@/utils/annotations'
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay";
export default {
name: "CheckboxInput",
  components: {InputErrorDisplay},
  props: ["value", "config", "document", "state", "msgError", "msgSuccess"],
  computed: {
    options(){
      if(this.config && this.config.options){
        return generateBVOptions(this.config.options, this.document)
      }
      return null
    },
    inputVal: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    },
  },

}
</script>

<style scoped>

</style>
