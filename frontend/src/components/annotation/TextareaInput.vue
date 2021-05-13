<template>
  <div>
    <BTextarea :name="config.name" v-model="inputVal" :state="state"></BTextarea>
    <b-form-invalid-feedback :state="state">
      Text must not be empty.
    </b-form-invalid-feedback>
    <b-form-valid-feedback :state="state">
      Looks Good.
    </b-form-valid-feedback>
  </div>
</template>

<script>
export default {
name: "TextareaInput",
  props: ["value", "config", "state"],
  computed: {
    inputVal: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    }
  }
}
</script>

<style scoped>

</style>
