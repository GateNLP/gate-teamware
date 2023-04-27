<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess" label-cols=3>
    <b-form-group :id="config.name">

      <b-form-radio 
        v-for="(option, idx) in options"
        :key="option.value"
        v-model="inputVal"
        :value="option.value"
        :state="state"
        :inline="config.orientation!=='vertical'"
        :name="config.name"
        >
          {{ option.text }}
          <b-icon-question-circle v-if="option.helptext != null" :id="config.name + '__opt' + idx" class="annotation-help-prompt"></b-icon-question-circle>
          <b-tooltip v-if="option.helptext != null" :target="config.name + '__opt' + idx" :title="option.helptext"></b-tooltip>
        </b-form-radio>
    </b-form-group>
  </InputErrorDisplay>
</template>

<script>
import { generateBVOptions } from '@/utils/annotations'
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay";
export default {
  name: "RadioInput",
  components: {InputErrorDisplay},
  props: ["value","config", "document", "state", "msgError", "msgSuccess"],
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
