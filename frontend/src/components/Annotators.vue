<template>
  <div>
    <h2 class="mt-2 mb-2">Annotators Management
      <b-icon-question-circle id="project-annotators-help" scale="0.5"
                              style="cursor:pointer;"></b-icon-question-circle>
    </h2>
    <b-popover target="project-annotators-help" triggers="hover" placement="bottom">
      Add annotators to the project by clicking on the list of names in the <strong>right column</strong>. Current
      annotators can be removed
      by clicking on the names in the <strong>left column</strong>. Removing annotators does not delete their
      completed annotations
      but will stop their current pending annotation task.

    </b-popover>
    <b-button-toolbar class="mt-2 mb-2">
      <b-button-group>
        <b-button :variant="loadingVariant" :disabled="loading" @click="refreshAnnotatorsHandler"
                  title="Refresh annotator list.">
          <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
          Refesh
        </b-button>
      </b-button-group>
    </b-button-toolbar>

    <div class="row">
      <div class="col-6">
        <h5>Current annotators of the project</h5>

        <b-form-input v-model="projectAnnotatorSearch" placeholder="Search by username or email"></b-form-input>

        <br>

        <b-list-group id="projectAnnotators">
          <b-list-group-item href="#" v-for="annotator in projectAnnotatorsPaginated" v-bind:key="annotator.id"
                             @click="removeAnnotator(annotator.username)"
                             class="d-flex justify-content-between align-items-center"
                             v-b-tooltip.hover :title="annotator.email">
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
      <div class="col-6">
        <h5>Add annotator to project</h5>

        <b-form-input v-model="possibleAnnotatorSearch" placeholder="Search by username or email"></b-form-input>

        <br>

        <b-list-group id="possibleAnnotators">
          <b-list-group-item href="#" v-for="annotator in possibleAnnotatorsPaginated" v-bind:key="annotator.id"
                             @click="addAnnotator(annotator.username)"
                             class="d-flex justify-content-between align-items-center"
                             v-b-tooltip.hover :title="annotator.email">
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
      loading: false,
    }
  },
  props: {
    projectID: {
      type: String,
      default: null,
    }
  },
  methods: {
    ...mapActions(["getPossibleAnnotators", "addProjectAnnotator", "removeProjectAnnotator", "getProjectAnnotators"]),
    async updateAnnotators() {

      this.possibleAnnotators = await this.getPossibleAnnotators();
      this.projectAnnotators = await this.getProjectAnnotators(this.projectID);

    },
    async addAnnotator(username) {
      this.setLoading(true)
      await this.addProjectAnnotator({projectID: this.projectID, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    async removeAnnotator(username) {
      this.setLoading(true)
      await this.removeProjectAnnotator({projectID: this.projectID, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    searchAnnotators(annotators, searchString) {
      const regEx = new RegExp(searchString);
      const result = _.filter(annotators, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
      return result
    },
    async refreshAnnotatorsHandler(){
      this.setLoading(true)
      await this.updateAnnotators()
      this.$emit("updated")
      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
  },
  mounted() {
    this.updateAnnotators();
  },
  computed: {
    possibleAnnotatorsFiltered() {
      return this.searchAnnotators(this.possibleAnnotators, this.possibleAnnotatorSearch);
    },
    projectAnnotatorsFiltered() {
      return this.searchAnnotators(this.projectAnnotators, this.projectAnnotatorSearch);
    },
    possibleAnnotatorsPaginated() {
      return this.possibleAnnotatorsFiltered.slice(
          (this.currentPagePossibleAnnotators - 1) * this.perPage,
          this.currentPagePossibleAnnotators * this.perPage
      )
    },
    projectAnnotatorsPaginated() {
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
    },
    loadingVariant() {
      if (this.loading) {
        return "secondary"
      } else {
        return "primary"
      }
    },

  }
}
</script>

<style scoped>

</style>
