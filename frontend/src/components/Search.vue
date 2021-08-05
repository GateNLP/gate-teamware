<template>
  <div>
    <b-form @submit.prevent="$emit('input', searchStr )">
      <b-input-group>
        <b-input v-model="searchStr" name="searchItem" value="" placeholder="Search..."></b-input>
        <b-input-group-append>
          <b-button type="submit">
            <b-icon-search></b-icon-search>
            Search
          </b-button>
        </b-input-group-append>
      </b-input-group>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      searchStr: null,
    }
  }
}
</script>

<style scoped>

</style>
