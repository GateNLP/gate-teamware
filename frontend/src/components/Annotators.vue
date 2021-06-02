<template>
  <div class="container">
    <div class="row">
      <div class="col-4">
        <h5>Current annotators of the project</h5>

        <b-form-input v-model="projectAnnotatorSearch" placeholder="Search by username or email"></b-form-input>

        <br>

        <b-list-group id="projectAnnotators">
          <b-list-group-item href="#" v-for="annotator in projectAnnotatorsPaginated" v-bind:key="annotator.id"
            @click="removeAnnotator(annotator.username)"
            class="d-flex justify-content-between align-items-center">
            {{ annotator.username }}
            <b-icon icon="person-x-fill" aria-hidden="true" variant="danger"></b-icon>
          </b-list-group-item>
        </b-list-group>

        <br>

        <b-pagination
          v-model="currentPageProjectAnnotators"
          :total-rows="rowsProjectAnnotators"
          :per-page="perPage"
          aria-controls="projectAnnotators"
          align="center"
        ></b-pagination>

      </div>
      <div class="col-4">
        <h5>Add annotator to project</h5>

        <b-form-input v-model="possibleAnnotatorSearch" placeholder="Search by username or email"></b-form-input>

        <br>

        <b-list-group id="possibleAnnotators">
          <b-list-group-item href="#" v-for="annotator in possibleAnnotatorsPaginated" v-bind:key="annotator.id"
            @click="addAnnotator(annotator.username)"
            class="d-flex justify-content-between align-items-center">
            {{ annotator.username }}
            <b-icon icon="person-plus-fill" aria-hidden="true" variant="success"></b-icon>
          </b-list-group-item>
        </b-list-group>

        <br>

        <b-pagination
          v-model="currentPagePossibleAnnotators"
          :total-rows="rowsPossibleAnnotators"
          :per-page="perPage"
          aria-controls="possibleAnnotators"
          align="center"
        ></b-pagination>

      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";

export default {
  name: "Annotators",
  data() {
    return {
      possibleAnnotators: [],
      possibleAnnotatorSearch: '',
      projectAnnotators: [],
      projectAnnotatorSearch: '',
      currentPageProjectAnnotators: 1,
      currentPagePossibleAnnotators: 1,
      perPage: 10,
    }
  },
  props:{
    projectID: {
      type: String,
      default: null,
    }
  },
  methods: {
    ...mapActions(["getPossibleAnnotators", "addProjectAnnotator", "removeProjectAnnotator", "getProjectAnnotators"]),
    async updateAnnotators(){
      this.possibleAnnotators = await this.getPossibleAnnotators();
      this.projectAnnotators = await this.getProjectAnnotators(this.projectID);
    },
    async addAnnotator(username){
      await this.addProjectAnnotator({ projectID: this.projectID, username: username });
      this.updateAnnotators();
    },
    async removeAnnotator(username){
      await this.removeProjectAnnotator({ projectID: this.projectID, username: username });
      this.updateAnnotators();
    },
    searchAnnotators(annotators,searchString){
      const regEx = new RegExp(searchString);
      const result = _.filter(annotators, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
      return result
    }
  },
  mounted(){
    this.updateAnnotators();
  },
  computed:{
    possibleAnnotatorsFiltered(){
      return this.searchAnnotators(this.possibleAnnotators,this.possibleAnnotatorSearch);
    },
    projectAnnotatorsFiltered(){
      return this.searchAnnotators(this.projectAnnotators,this.projectAnnotatorSearch);
    },
    possibleAnnotatorsPaginated(){
      return this.possibleAnnotatorsFiltered.slice(
        (this.currentPagePossibleAnnotators - 1) * this.perPage,
        this.currentPagePossibleAnnotators * this.perPage
      )
    },
    projectAnnotatorsPaginated(){
      return this.projectAnnotatorsFiltered.slice(
        (this.currentPageProjectAnnotators - 1) * this.perPage,
        this.currentPageProjectAnnotators * this.perPage
      )
    },
    rowsPossibleAnnotators() {
      return this.possibleAnnotatorsFiltered.length
    },
    rowsProjectAnnotators() {
      return this.projectAnnotatorsFiltered.length
    }
  }
}
</script>

<style scoped>

</style>