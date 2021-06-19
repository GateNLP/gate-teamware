<template>
  <div>
    <div class="d-flex justify-content-center">
      <BPagination v-model="currentPage" :total-rows="numDocs" :per-page="docsPerPage"></BPagination>
    </div>

    <BCard v-for="doc in filteredDocs" :key="doc.id" class="mb-2">
      <BMedia>
        <template v-slot:aside>
          <div>
            <b-icon-file-earmark-text-fill style="width: 1.5em; height: auto"></b-icon-file-earmark-text-fill>
          </div>
        </template>

        <div class="d-flex justify-content-between">
          <div>
            <div>
              <strong>ID:{{ doc.id }}</strong>
            </div>
            <div>
              <b-icon-clock class="mr-2"></b-icon-clock>{{ doc.created | datetime }}
            </div>
          </div>

          <div>
            <b-badge variant="success" class="mr-2" title="Completed annotations">
              <b-icon-pencil-fill></b-icon-pencil-fill>
              {{ doc.completed }}
            </b-badge>
            <b-badge variant="danger" class="mr-2" title="Rejected annotations">
              <b-icon-x-square-fill></b-icon-x-square-fill>
              {{ doc.rejected }}
            </b-badge>
            <b-badge variant="warning" class="mr-2" title="Timed out annotations">
              <b-icon-clock></b-icon-clock>
              {{ doc.timed_out }}
            </b-badge>
            <b-badge variant="secondary" class="mr-2" title="Aborted annotations">
              <b-icon-stop-fill></b-icon-stop-fill>
              {{ doc.aborted }}
            </b-badge>
            <b-badge variant="primary" class="mr-2" title="Pending annotations">
              <b-icon-play-fill></b-icon-play-fill>
              {{ doc.pending }}
            </b-badge>

          </div>

        </div>

        <AsyncJsonDisplay
            class="mt-2"
            :fetch-function="getDocumentContent"
            :fetch-param="doc.id"
            show-text="Show document data"
            hide-text="Hide document data">
        </AsyncJsonDisplay>


        <BCard v-for="anno in doc.annotations" :key="anno.id" class="mt-4">

          <BMedia>
            <template v-slot:aside>
              <b-badge v-if="anno.completed" variant="success" class="mr-2"  title="Annotation completed">
                <b-icon-pencil-fill style="width: 1.5em; height: auto;"></b-icon-pencil-fill>
              </b-badge>
              <b-badge v-else-if="anno.rejected" variant="danger" class="mr-2" title="Annotation rejected">
                <b-icon-x-square-fill style="width: 1.5em; height: auto;"></b-icon-x-square-fill>
              </b-badge>
              <b-badge v-else-if="anno.timed_out" variant="warning" class="mr-2" title="Annotation timed out">
                <b-icon-clock style="width: 1.5em; height: auto;"></b-icon-clock>
              </b-badge>
              <b-badge v-else-if="anno.aborted" variant="secondary" class="mr-2" title="Annotation aborted">
                <b-icon-stop-fill style="width: 1.5em; height: auto;"></b-icon-stop-fill>
              </b-badge>
              <b-badge v-else variant="primary" class="mr-2" title="Annotation still pending">
                <b-icon-play-fill style="width: 1.5em; height: auto;"></b-icon-play-fill>
              </b-badge>
            </template>
            <div>
              <strong>ID: {{ anno.id }}</strong>
            </div>
            <div title="Annotated by">
              <b-icon-person-fill></b-icon-person-fill>
              {{ anno.annotated_by }}
            </div>

            <div>
              <b-icon-clock></b-icon-clock>
              Created: {{ anno.created | datetime }}
            </div>
            <div v-if="anno.completed">
              <b-icon-clock></b-icon-clock>
              Completed: {{ anno.completed | datetime }}
            </div>
            <div v-else-if="anno.rejected">
              <b-icon-clock></b-icon-clock>
              Rejected: {{ anno.rejected | datetime }}
            </div>
            <div v-else-if="anno.timed_out">
              <b-icon-clock></b-icon-clock>
              Time out: {{ anno.timed_out | datetime }}
            </div>
            <div v-else-if="anno.aborted">
              <b-icon-clock></b-icon-clock>
              Aborted at: {{ anno.aborted | datetime }}
            </div>
            <div v-else>
              <b-icon-clock></b-icon-clock>
              Will time out at: {{ anno.times_out_at | datetime }}
            </div>

            <AsyncJsonDisplay v-if="anno.completed"
                class="mt-2"
                :fetch-function="getAnnotationContent"
                :fetch-param="anno.id"
                show-text="Show annotation data"
                hide-text="Hide annotation data">

            </AsyncJsonDisplay>
          </BMedia>

        </BCard>

      </BMedia>


    </BCard>

    <div class="d-flex justify-content-center">
      <BPagination v-model="currentPage" :total-rows="numDocs" :per-page="docsPerPage"></BPagination>
    </div>


  </div>


</template>

<script>
import {mapActions} from "vuex";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import AsyncJsonDisplay from "@/components/AsyncJsonDisplay";

export default {
  name: "DocumentsList",
  components: {AsyncJsonDisplay},
  data() {
    return {
      currentPage: 1,
      docsPerPage: 10,
    }
  },
  computed: {
    numDocs() {
      return this.documents.length
    },
    filteredDocs() {

      if (this.numDocs <= 0)
        return []

      let startIndex = (this.currentPage - 1) * this.docsPerPage
      let endIndex = startIndex + this.docsPerPage
      if (endIndex > this.numDocs) {
        endIndex = this.numDocs
      }

      let out_docs = []
      for (let i = startIndex; i < endIndex; i++) {
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
  },
  methods: {
    ...mapActions(["getDocumentContent", "getAnnotationContent"])
  }
}
</script>

<style scoped>

</style>
