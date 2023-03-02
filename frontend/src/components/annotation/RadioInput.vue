<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">
    <b-form-radio-group v-model="inputVal"  :name="config.name" :options="options" :state="state" :stacked="config.orientation === 'vertical'"></b-form-radio-group>
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
