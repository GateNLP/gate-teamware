<template>
  <div class="container">
    <h1>Annotating: {{local_project.name}}</h1>
    <b-row>
      <b-col md="4">
        <b-list-group v-if="local_project && local_project.configuration && documents">
          <b-list-group-item v-for="document in documents">
            <b-link :to="`/annotate/${projectId}/${document.id}`">Document {{document.id}}</b-link>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col>
        <div v-if="local_project && local_project.configuration && annotateDocument">
      <AnnotationRenderer :config="local_project.configuration" :document="annotateDocument" @submit="submitHandler"></AnnotationRenderer>
    </div>
    <div v-else>
      Invalid document for annotation
    </div>

      </b-col>
    </b-row>


  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import AnnotationRenderer from "@/components/AnnotationRenderer";

export default {
  name: "Annotate",
  components: {AnnotationRenderer},
  data() {
    return {
      local_project: null,
      documents: null,
    }
  },
  computed: {
    ...mapState(["projects"]),
    projectId() {
      return this.$route.params.pid
    },
    docId() {
      return this.$route.params.did
    },
    annotateDocument(){
      if(this.docId && this.documents){
        for(let doc of this.documents){
          if(String(doc.id) === this.docId){
            return doc.data
          }
        }
      }

      return null
    }
  },
  methods: {
    ...mapActions(["getProjects", "getProjectDocuments", "addAnnotation"]),
    submitHandler(value){
      this.addAnnotation({docId: this.docId, annotation: value})
    }
  },
  async mounted() {
    await this.getProjects();
    if (this.projectId) {
      for (let project of this.projects) {
        if (String(project.id) === this.projectId) {
          this.local_project = _.cloneDeep(project)
        }
      }
      this.documents = await this.getProjectDocuments(this.projectId)
    }
  }
}
</script>

<style scoped>

</style>
