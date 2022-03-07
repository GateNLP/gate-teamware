<template>
  <b-overlay :show="isLoading">
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
  </b-overlay>
</template>

<script>
/**
 * Top and bottom pagination component with page size selector. Designed to be used
 * with async calls.
 *
 * Component has a single default slot with variable pageItems e.g.
 * <PaginationAsync v-slot:default="{pageItems}">
 *   <div v-for="item in pageItems" :key="item.key">
 *     ....
 *   </div>
 * </PaginationAsync>
 *
 * Events:
 * page-size-change
 */
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
    /**
     * Current page number, index starts from 1
     */
    value: {
      default: 1
    },
    /**
     * Total number of items
     */
    numItems: {
      default: 0
    },
    /**
     * Number of items to be displayed per page
     */
    itemsPerPage: {
      default: 10
    },
    /**
     * Items to be shown on the current page
     */
    items: {
      default(){
        return []
      }
    },
    /**
     * Is page loading
     */
    isLoading: {
      default: false,
      type: Boolean,
    },
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
        this.$emit("page-size-change", newValue)
      }
    }
  },
}
</script>

<style scoped>

</style>
