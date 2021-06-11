<template>
  <div>
    <BCard v-for="doc in filteredDocs" :key="doc.id" class="mb-2">
      <BMedia>
        <template v-slot:aside>
          <b-icon-file-earmark-text-fill style="width: 1.5em; height: auto"></b-icon-file-earmark-text-fill>
          <strong>{{ doc.id }}</strong>
        </template>

        <div>
          {{doc.created}}
        </div>
        <div>
          <b-badge variant="success" class="mr-2">
          <b-icon-pencil-fill ></b-icon-pencil-fill>
          {{doc.completed}}
        </b-badge>
        <b-badge variant="danger" class="mr-2">
          <b-icon-x-square-fill></b-icon-x-square-fill>
          {{doc.rejected}}
        </b-badge>
        <b-badge variant="warning" class="mr-2">
          <b-icon-clock></b-icon-clock>
          {{doc.timed_out}}
        </b-badge>
        <b-badge variant="primary" class="mr-2">
          <b-icon-play-fill></b-icon-play-fill>
          {{doc.pending}}
        </b-badge>

        </div>

        <BCard  v-for="anno in doc.annotations" :key="anno.id" class="mt-4">

          <BMedia>
          <template v-slot:aside>
          <b-icon-pencil-square style="width: 1.5em; height: auto"></b-icon-pencil-square>
          <strong>{{ anno.id }}</strong>
        </template>

          {{anno.annotated_by}}
          {{anno.created}}
        </BMedia>

        </BCard>

      </BMedia>


    </BCard>

    <BPagination v-model="currentPage" :total-rows="numDocs" :per-page="docsPerPage"></BPagination>

  </div>


</template>

<script>
export default {
  name: "DocumentsList",
  data(){
    return {
      currentPage: 1,
      docsPerPage: 10,
    }
  },
  computed: {
    numDocs(){
      return this.documents.length
    },
    filteredDocs(){

      if(this.numDocs <= 0)
        return []

      let startIndex = (this.currentPage-1)*this.docsPerPage
      let endIndex = startIndex+this.docsPerPage
      if(endIndex > this.numDocs){
        endIndex = this.numDocs
      }

      let out_docs = []
      for(let i = startIndex; i < endIndex; i++){
        out_docs.push(this.documents[i])
      }

      return out_docs
    }
  },
  props: {
    documents: {
      type: Array,
      default() {
        return []
      }
    }
  }
}
</script>

<style scoped>

</style>
