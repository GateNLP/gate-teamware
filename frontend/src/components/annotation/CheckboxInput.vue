<template>
  <div>
    <b-form-checkbox-group v-model="inputVal" :name="config.name" :options="options" :state="state"></b-form-checkbox-group>
    <b-form-invalid-feedback :state="state">
      At least one item must be selected.
    </b-form-invalid-feedback>
    <b-form-valid-feedback :state="state">
      Looks Good.
    </b-form-valid-feedback>
  </div>

</template>

<script>
import { generateBVOptions } from '@/utils'
export default {
name: "CheckboxInput",
  props: ["value", "config", "state"],
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
