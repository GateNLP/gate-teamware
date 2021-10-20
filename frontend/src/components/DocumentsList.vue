<template>
  <div>
    <Search class="mt-4" @input="searchDocs"></Search>
    <Pagination class="mt-4" :items="filteredDocuments" v-slot:default="{ pageItems }">
      <BCard v-for="doc in pageItems" :key="doc.id" :class="{ 'mb-2': true, 'selectedDoc': isDocSelected(doc)}">
        <BMedia>
          <template v-slot:aside>
            <div @click="toggleDocument(doc)" style="cursor: pointer">
              <b-badge variant="primary" :class="{'docBgSelected': isDocSelected(doc)}">
                <b-icon-file-earmark-check v-if="isDocSelected(doc)"
                                         :class="{ 'docIcon': true, 'docIconSelected': isDocSelected(doc)}"></b-icon-file-earmark-check>
              <b-icon-file-earmark-text-fill v-else
                                             :class="{ 'docIcon': true, 'docIconSelected': isDocSelected(doc)}"></b-icon-file-earmark-text-fill>

              </b-badge>


            </div>
          </template>
          <div class="d-flex justify-content-between">
            <div>
              <div>
                <strong>ID:{{ doc.id }}</strong>
              </div>
              <div>
                <b-icon-clock class="mr-2"></b-icon-clock>
                {{ doc.created | datetime }}
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


          <BCard v-for="anno in doc.annotations" :key="anno.id"
                 :class="{ 'mt-4': true, 'selectedAnnotation': isAnnotationSelected(anno)}">

            <BMedia>
              <template v-slot:aside>
                <div @click="toggleAnnotation(anno, doc)" style="cursor: pointer">
                  <b-badge v-if="anno.completed" variant="success" :class="{'mr-2': true, 'docBgSelected': isAnnotationSelected(anno)} " title="Annotation completed">
                    <b-icon-pencil-fill :class="{ 'docIcon': true, 'docIconSelected': isAnnotationSelected(anno)}"></b-icon-pencil-fill>
                  </b-badge>
                  <b-badge v-else-if="anno.rejected" variant="danger" :class="{'mr-2': true, 'docBgSelected': isAnnotationSelected(anno)} " title="Annotation rejected">
                    <b-icon-x-square-fill :class="{ 'docIcon': true, 'docIconSelected': isAnnotationSelected(anno)}"></b-icon-x-square-fill>
                  </b-badge>
                  <b-badge v-else-if="anno.timed_out" variant="warning" :class="{'mr-2': true, 'docBgSelected': isAnnotationSelected(anno)} " title="Annotation timed out">
                    <b-icon-clock :class="{ 'docIcon': true, 'docIconSelected': isAnnotationSelected(anno)}"></b-icon-clock>
                  </b-badge>
                  <b-badge v-else-if="anno.aborted" variant="secondary" :class="{'mr-2': true, 'docBgSelected': isAnnotationSelected(anno)} " title="Annotation aborted">
                    <b-icon-stop-fill :class="{ 'docIcon': true, 'docIconSelected': isAnnotationSelected(anno)}"></b-icon-stop-fill>
                  </b-badge>
                  <b-badge v-else variant="primary" :class="{'mr-2': true, 'docBgSelected': isAnnotationSelected(anno)} " title="Annotation still pending">
                    <b-icon-play-fill :class="{ 'docIcon': true, 'docIconSelected': isAnnotationSelected(anno)}"></b-icon-play-fill>
                  </b-badge>
                </div>
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

    </Pagination>
  </div>


</template>

<script>
import {mapActions} from "vuex";
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import AsyncJsonDisplay from "@/components/AsyncJsonDisplay";
import Pagination from "@/components/Pagination";
import Search from "@/components/Search";
import _ from "lodash"

export default {
  name: "DocumentsList",
  components: {Search, Pagination, AsyncJsonDisplay},
  data() {
    return {
      searchStr: "",
      selectedDocs: new Set(),
      selectedAnnotations: new Set(),
    }
  },
  props: {
    documents: {
      type: Array,
      default() {
        return []
      }
    },
  },
  computed: {
    filteredDocuments() {

      //Returns all if no or empty search string
      if (!this.searchStr || this.searchStr.trim().length < 1)
        return this.documents

      let searchStr = this.searchStr

      // Currently searching for project names only
      let result = _.filter(
          this.documents,
          function (o) {
            return _.includes(_.lowerCase(o.id), _.lowerCase(searchStr))
          }
      )
      return result

    }
  },
  methods: {
    ...mapActions(["getDocumentContent", "getAnnotationContent"]),
    searchDocs(searchStr) {
      this.searchStr = searchStr
    },
    emitSelectionList(){

      // Forces vue to track the set change
      this.selectedDocs = new Set(this.selectedDocs)
      this.selectedAnnotations = new Set(this.selectedAnnotations)

      this.$emit("selection-changed",
          {
            documents: [...this.selectedDocs],
            annotations: [...this.selectedAnnotations],
          })

    },
    selectDocument(doc, doSelect, emitEvent=true){
      if(doSelect){
        this.selectedDocs.add(doc.id)
        for(let anno of doc.annotations){
          this.selectedAnnotations.add(anno.id)
        }
      }
      else{
        this.selectedDocs.delete(doc.id)
        for(let anno of doc.annotations){
          this.selectedAnnotations.delete(anno.id)
        }
      }

      if(emitEvent)
        this.emitSelectionList()

    },
    toggleDocument(doc) {
      this.selectDocument(doc, !this.selectedDocs.has(doc.id))

    },
    isDocSelected(doc) {
      return this.selectedDocs.has(doc.id)
    },
    selectAnnotation(anno, doSelect, doc, emitEvent=true){
      //Can't change selection if document is already selected
      if(this.isDocSelected(doc))
        return

      if (doSelect)
        this.selectedAnnotations.add(anno.id)
      else
        this.selectedAnnotations.delete(anno.id)


      if(emitEvent)
        this.emitSelectionList()

    },
    toggleAnnotation(anno, doc) {
      this.selectAnnotation(anno, !this.selectedAnnotations.has(anno.id), doc)
    },
    isAnnotationSelected(anno) {
      return this.selectedAnnotations.has(anno.id)
    },
    clearDocumentSelection(doEmitEvent=true){
      for(let doc of this.documents){
        this.selectDocument(doc, false, false)
      }
      if(doEmitEvent)
        this.emitSelectionList()
    },
    clearAnnotationSelection(doEmitEvent=true){
      for(let doc in this.documents){
        for(let anno in doc.annotations){
          this.selectAnnotation(anno, false, doc,false)
        }
      }

      if(doEmitEvent)
        this.emitSelectionList()

    },
    selectAllDocuments(doEmitEvent=true){
      for(let doc of this.documents){
        this.selectDocument(doc, true, false)
      }

      if(doEmitEvent)
        this.emitSelectionList()

    },
    selectAllAnnotations(doEmitEvent=true){
      for(let doc of this.documents){
        for(let anno of doc.annotations){
          this.selectAnnotation(anno, true, doc, false)
        }
      }

      if(doEmitEvent)
        this.emitSelectionList()

    },
  },
  watch:{
    documents(val){
      //Clear all selections when documents prop are set
      this.selectedDocs = new Set()
      this.selectedAnnotations = new Set()
      this.emitSelectionList()

    }
  }
}
</script>

<style scoped>

.selectedDoc {
  background: #cbcbcb;
}

.selectedAnnotation {
  background: #b3b3b3;
}

.docBgSelected{
  background: #fff;
}

.docIcon {
  width: 1.5em;
  height: auto
}

.docIconSelected{
  color: black;
}

</style>
