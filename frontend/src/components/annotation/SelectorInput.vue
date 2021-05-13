<template>
  <div>
    <BFormSelect :options="options" v-model="inputVal" :state="state"></BFormSelect>
    <b-form-invalid-feedback :state="state">
      An item must be selected.
    </b-form-invalid-feedback>
    <b-form-valid-feedback :state="state">
      Looks Good.
    </b-form-valid-feedback>
  </div>

</template>

<script>

import { generateBVOptions } from '@/utils'
export default {
  name: "SelectorInput",
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
