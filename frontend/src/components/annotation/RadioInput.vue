<template>
  <div>
    <b-form-radio-group v-model="inputVal"  :name="config.name" :options="options" :state="state"></b-form-radio-group>
    <b-form-invalid-feedback :state="state">
      An option must be selected.
    </b-form-invalid-feedback>
    <b-form-valid-feedback :state="state">
      Looks Good.
    </b-form-valid-feedback>
  </div>

</template>

<script>
import { generateBVOptions } from '@/utils'
export default {
  name: "RadioInput",
  props: ["value","config", "state"],
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
