<template>
  <div>
    <b-form-group label="Project Configuration">
      <b-textarea v-model="jsonStr" @change="jsonStrChangeHandler" rows="30"></b-textarea>
    </b-form-group>
    <div class="text-danger" v-if="jsonStr && json_error && valid_json === false">{{ json_error }}</div>
    <div class="text-success" v-if="valid_json === true">Valid JSON ✔</div>
  </div>

</template>

<script>
export default {
  name: "JsonEditor",
  data() {
    return {
      jsonStr: "",
      valid_json: null,
      json_error: "",
    }
  },
  props: {
    value: {
      default: null
    }
  },
  methods: {
    jsonStrChangeHandler(e){
      this.valid_json = this.validateJSON(this.jsonStr)
      if(this.valid_json){
        this.$emit('input', JSON.parse(this.jsonStr))
      }
    },
    validateJSON(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            this.json_error = JSON.stringify(e.message);
            return false;
        }
        return true;
    },
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue){
        if(newValue){
          this.jsonStr = JSON.stringify(newValue, null, 2)
        }
        else{
          this.jsonStr = ""
        }
      }
    }
  }
}
</script>

<style scoped>

</style>
