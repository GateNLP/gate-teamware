<template>
  <div>
    <slot></slot>
    <b-form-invalid-feedback :state="state">
      {{errorMessage}}
    </b-form-invalid-feedback>
    <b-form-valid-feedback :state="state">
      {{successMessage}}
    </b-form-valid-feedback>
  </div>
</template>

<script>
export default {
  name: "InputErrorDisplay",
  props: ["state", "msgError", "msgSuccess"],
  computed: {
    errorMessage(){
      if(this.msgError)
        return this.msgError

      return "Annotation required."
    },
    successMessage(){
      if(this.msgSuccess)
        return this.msgSuccess

      return "Annotation valid."
    },
  }
}
</script>

<style scoped>

</style>
