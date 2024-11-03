<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">

    <b-form-checkbox-group 
      v-model="inputVal"
      :stacked="config.orientation=='vertical'"
      :name="config.name"
      >
      
      <b-form-checkbox 
        :key="option.value" 
        :value="option.value" 
        :state="state"
        v-for="(option, idx) in options"
        >
        <span v-if="option.html" v-html="option.html"></span>
        <span v-else>{{ option.text }}</span>
        <b-icon-question-circle v-if="option.helptext != null" :id="config.name + '__opt' + idx" class="annotation-help-prompt"></b-icon-question-circle>
        <b-tooltip v-if="option.helptext != null" :target="config.name + '__opt' + idx" :title="option.helptext"></b-tooltip>
      </b-form-checkbox>

    </b-form-checkbox-group>
  </InputErrorDisplay>
</template>

<script>
import { generateBVOptions } from '@/utils/annotations'
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay.vue";
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
