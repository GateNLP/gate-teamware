<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">
    <BInput :name="config.name" v-model="inputVal" :state="state"/>
  </InputErrorDisplay>
</template>

<script>
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay.vue";

export default {
  name: "TextInput",
  components: {InputErrorDisplay},
  props: ["value", "config", "state", "msgError", "msgSuccess"],
  computed: {
    inputVal: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    },
  },
  methods: {
    validate(){
      return true
    }
  }
}
</script>

<style scoped>

</style>
