<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">
    <b-form-checkbox-group v-model="inputVal" :name="config.name" :options="options" :state="state"></b-form-checkbox-group>
  </InputErrorDisplay>
</template>

<script>
import { generateBVOptions } from '@/utils'
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay";
export default {
name: "CheckboxInput",
  components: {InputErrorDisplay},
  props: ["value", "config", "state", "msgError", "msgSuccess"],
  computed: {
    options(){
      if(this.config && this.config.options){
        return generateBVOptions(this.config.options)
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
