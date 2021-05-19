<template>
  <div>
    <BInput :name="config.name" v-model="inputVal" :state="state"/>
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
  name: "TextInput",
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
