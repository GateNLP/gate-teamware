<template>
  <InputErrorDisplay :state="state" :msg-error="msgError" :msg-success="msgSuccess">
    <BTextarea :name="config.name" v-model="inputVal" :state="state"></BTextarea>
  </InputErrorDisplay>
</template>

<script>
import InputErrorDisplay from "@/components/annotation/InputErrorDisplay";

export default {
name: "TextareaInput",
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
  }
}
</script>

<style scoped>

</style>
