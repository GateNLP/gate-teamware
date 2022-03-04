<template>
  <div>
    <div class="d-flex justify-content-between">
      <div></div>
      <BPagination v-model="currentPage" :total-rows="numItems" :per-page="itemsPerPageLocal"></BPagination>
      <BSelect v-model="itemsPerPageLocal" :options="itemsPerPageOption" style="max-width: 6em" title="Items per page"></BSelect>
    </div>


      <slot :pageItems="items"></slot>

    <div class="d-flex justify-content-between">
      <div></div>
      <BPagination v-model="currentPage" :total-rows="numItems" :per-page="itemsPerPageLocal"></BPagination>
      <BSelect v-model="itemsPerPageLocal" :options="itemsPerPageOption" style="max-width: 6em" title="Items per page"></BSelect>
    </div>
  </div>
</template>

<script>
export default {
  name: "PaginationAsync",
  data() {
    return {
      itemsPerPageOption: [
        { value: 5, text: "5"},
          { value: 10, text: "10"},
          { value: 50, text: "50"},
          { value: 100, text: "100"},
      ],
    }
  },
  props: {
    value: { //Current page number
      default: 1
    },
    numItems: {
      default: 0
    },
    itemsPerPage: {
      default: 10
    },
    items: {
      default(){
        return []
      }
    }
  },
  computed: {
    currentPage: {
      get(){
        return this.value
      },
      set(newValue){
        this.$emit("input", newValue)
      }
    },
    itemsPerPageLocal:{
      get(){
        return this.itemsPerPage
      },
      set(newValue){
        this.$emit("itemPerPageChange", newValue)
      }
    }
  },
}
</script>

<style scoped>

</style>
