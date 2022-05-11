<template>
  <div>
    <div class="d-flex justify-content-between">
      <div></div>
      <BPagination v-model="currentPage" :total-rows="numItems" :per-page="itemsPerPage"></BPagination>
      <BSelect v-model="itemsPerPage" :options="itemsPerPageOption" style="max-width: 6em" title="Items per page"></BSelect>
    </div>


      <slot :pageItems="pageItems"></slot>

    <div class="d-flex justify-content-between">
      <div></div>
      <BPagination v-model="currentPage" :total-rows="numItems" :per-page="itemsPerPage"></BPagination>
      <BSelect v-model="itemsPerPage" :options="itemsPerPageOption" style="max-width: 6em" title="Items per page"></BSelect>
    </div>
  </div>
</template>

<script>
/**
 * Top and bottom pagination component with page size selector.
 *
 * Component has a single default slot with variable pageItems e.g.
 * <Pagination v-slot:default="{pageItems}">
 *   <div v-for="item in pageItems" :key="item.key">
 *     ....
 *   </div>
 * </Pagination>
 */
export default {
  name: "Pagination",
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      itemsPerPageOption: [
        { value: 5, text: "5"},
          { value: 10, text: "10"},
          { value: 50, text: "50"},
          { value: 100, text: "100"},
      ]
    }
  },
  props: {
    /**
     * Full list of items to be displayed
     */
    items: {
      type: Array,
      default() {
        return []
      }
    },
  },
  computed: {
    numItems() {
      return this.items.length
    },
    pageItems(){

      if (this.numItems <= 0)
        return []

      let startIndex = (this.currentPage - 1) * this.itemsPerPage
      let endIndex = startIndex + this.itemsPerPage
      if (endIndex > this.numItems) {
        endIndex = this.numItems
      }

      let out_items = []
      for (let i = startIndex; i < endIndex; i++) {
        out_items.push(this.items[i])
      }

      return out_items

    }
  }

}
</script>

<style scoped>

</style>
