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
          <b-list-group-item href="#" v-for="annotator in projectAnnotatorsPaginated" v-bind:key="annotator.id">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div>
                <span :title="annotator.email"><strong>{{ annotator.username }}</strong></span>
              </div>
              <div class="d-flex align-items-end">

                <div class="mr-2">
                  <b-icon-check-square-fill v-if="annotator.status == 0" title="Annotator is active in project"
                                            variant="success"></b-icon-check-square-fill>
                  <b-icon-check-square-fill v-else title="Annotator not active in project"
                                            variant="secondary"></b-icon-check-square-fill>


                </div>
                <div class="mr-2">
                  <b-icon-pencil-square v-if="annotator.allowed_to_annotate" title="Annotator is allowed to annotate"
                                            variant="success"></b-icon-pencil-square>
                  <b-icon-pencil-square v-else title="Annotator not allowed to annotate"
                                            variant="secondary"></b-icon-pencil-square>


                </div>
                <div>
                  <b-icon-dash-circle-fill v-if="annotator.rejected" rotate="-45" variant="danger"
                                           title="Annotator rejected"></b-icon-dash-circle-fill>
                  <b-icon-dash-circle-fill v-else rotate="-45" variant="secondary"
                                           title="Annotator rejected"></b-icon-dash-circle-fill>
                </div>


              </div>

            </div>

            <b-row class="d-flex">
              <b-col :class="{stageActive:isAtTrainingStage(annotator)}">
                <div style="font-weight: bold">
                  Training
                </div>
                <div v-if="project.has_training_stage">
                  <div class="d-flex" title="Completed time">
                    <div class="mr-1">
                      <b-icon-clock></b-icon-clock>
                    </div>
                    <div>
                      <span v-if="annotator.training_completed">
                        {{ annotator.training_completed | datetime }}
                      </span>
                      <span v-else>-</span>
                    </div>
                  </div>
                  <div class="d-flex" title="Score">
                    <div class="mr-1">
                      <b-icon-check-square-fill></b-icon-check-square-fill>
                    </div>
                    <div>
                      {{ annotator.training_score }}
                    </div>
                  </div>
                </div>
                <div v-else>
                  <b-icon-x-square-fill></b-icon-x-square-fill>
                  Stage disabled
                </div>
              </b-col>
              <b-col :class="{stageActive:isAtTestStage(annotator)}">
                <div style="font-weight: bold">
                  Test
                </div>
                <div v-if="project.has_test_stage">
                  <div class="d-flex" title="Completed time">
                    <div class="mr-1">
                      <b-icon-clock></b-icon-clock>
                    </div>
                    <div>
                      <span v-if="annotator.test_completed">
                        {{ annotator.test_completed | datetime }}
                      </span>
                      <span v-else>-</span>
                    </div>
                  </div>
                  <div class="d-flex" title="Score">
                    <div class="mr-1">
                      <b-icon-check-square-fill></b-icon-check-square-fill>
                    </div>
                    <div>
                      {{ annotator.test_score }}
                    </div>
                  </div>
                </div>
                <div v-else>
                  <b-icon-x-square-fill></b-icon-x-square-fill>
                  Stage disabled
                </div>
              </b-col>
              <b-col :class="{stageActive:isAtAnnotationStage(annotator)}">
                <div style="font-weight: bold">
                  Annotation
                  <b-icon-exclamation-triangle-fill variant="warning" v-if="getAnnotationStageWarning(annotator)"
                    :title="getAnnotationStageWarning(annotator)">
                  </b-icon-exclamation-triangle-fill>
                </div>
                <div class="d-flex" title="Completed time">
                    <div class="mr-1">
                      <b-icon-clock></b-icon-clock>
                    </div>
                    <div>
                      <span v-if="annotator.test_completed">
                        {{ annotator.test_completed | datetime }}
                      </span>
                      <span v-else>-</span>
                    </div>
                  </div>
              </b-col>
              <b-col>
                <b-button-group vertical>
                  <b-button
                      :variant="getMakeAnnotatorBtnVariant(annotator)"
                      size="sm"
                      @click="allowAnnotation(annotator.username)"
                      :title="getMakeAnnotatorBtnTitle(annotator)"
                      :disabled="getMakeAnnotatorBtnDisabled(annotator)"
                  >
                    <b-icon-pencil-square></b-icon-pencil-square>
                    Make annotator
                  </b-button>
                  <b-button size="sm"
                            @click="removeAnnotator(annotator.username)"
                            :variant="getAnnotatorCompleteBtnVariant(annotator)"

                            :title="getAnnotatorCompleteBtnTitle(annotator)"
                            :disabled="getAnnotatorCompleteBtnDisabled(annotator)">
                    <b-icon icon="person-x-fill" aria-hidden="true"></b-icon>
                    Complete
                  </b-button>
                  <b-button size="sm"
                            :variant="getAnnotatorRejectBtnVariant(annotator)"
                            :title="getAnnotatorRejectBtnTitle(annotator)"
                            :disabled="getAnnotatorRejectBtnDisabled(annotator)"
                            @click="rejectAnnotator(annotator.username)">
                    <b-icon-dash-circle rotate="-45"></b-icon-dash-circle>
                    Reject
                  </b-button>
                </b-button-group>

              </b-col>
            </b-row>
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
    project: {
      type: Object,
      default: null,
    }
  },
  methods: {
    ...mapActions(["getPossibleAnnotators", "addProjectAnnotator", "removeProjectAnnotator", "getProjectAnnotators",
      "projectAnnotatorAllowAnnotation", "rejectProjectAnnotator"]),

    isAtTrainingStage(annotator){
      return annotator.status == 0 &&
          !this.isAtAnnotationStage(annotator) &&
          !annotator.training_completed &&
          this.project.has_training_stage

    },
    isAtTestStage(annotator){
      return annotator.status == 0 &&
          !this.isAtTrainingStage(annotator) &&
          !this.isAtAnnotationStage(annotator) &&
          !annotator.test_completed &&
          this.project.has_test_stage
    },
    isAtAnnotationStage(annotator){
      return annotator.status == 0 && annotator.allowed_to_annotate
    },
    getAnnotationStageWarning(annotator){
      if(!this.isAtTrainingStage(annotator) &&
      !this.isAtTestStage(annotator) &&
      !this.isAtAnnotationStage(annotator) &&
      annotator.status == 0){
        return "Annotator waiting for permission to annotate."
      }

      return null

    },
    getMakeAnnotatorBtnVariant(annotator) {
      if (annotator.allowed_to_annotate)
        return "secondary"
      else
        return "primary"
    },
    getMakeAnnotatorBtnTitle(annotator) {
      if (annotator.allowed_to_annotate)
        return "Annotator already allowed to annotate."
      else
        return "Allow annotator to annotate data, skipping training and testing stages."

    },
    getMakeAnnotatorBtnDisabled(annotator) {
      if ( annotator.allowed_to_annotate)
        return true

      return false
    },
    getAnnotatorCompleteBtnVariant(annotator) {
      if(annotator.status == 0)
        return "warning"
      else
        return "secondary"

    },
    getAnnotatorCompleteBtnTitle(annotator) {
      if (annotator.status == 0)
        return "Mark annotator as having completed annotation of the project and will be transferred to the available annotator pool."
      else
        return "Annotator not active in project"

    },
    getAnnotatorCompleteBtnDisabled(annotator) {
      return annotator.status != 0
    },
    getAnnotatorRejectBtnVariant(annotator) {
      if(annotator.status == 0)
        return "danger"
      else
        return "secondary"

    },
    getAnnotatorRejectBtnTitle(annotator) {
      if (annotator.status == 0)
        return "Mark annotator as having completed annotation of the project and will be transferred to the available annotator pool."
      else
        return "Annotator not active in project"

    },
    getAnnotatorRejectBtnDisabled(annotator) {
      return annotator.status != 0
    },
    async updateAnnotators() {

      this.possibleAnnotators = await this.getPossibleAnnotators(this.project.id);
      this.projectAnnotators = await this.getProjectAnnotators(this.project.id);

    },
    async addAnnotator(username) {
      this.setLoading(true)
      await this.addProjectAnnotator({projectID: this.project.id, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    async removeAnnotator(username) {
      this.setLoading(true)
      await this.removeProjectAnnotator({projectID: this.project.id, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    async rejectAnnotator(username) {
      this.setLoading(true)
      await this.rejectProjectAnnotator({projectID: this.project.id, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    async allowAnnotation(username) {
      this.setLoading(true)
      await this.projectAnnotatorAllowAnnotation({projectID: this.project.id, username: username});
      await this.updateAnnotators();
      this.$emit("updated")
      this.setLoading(false)
    },
    searchAnnotators(annotators, searchString) {
      const regEx = new RegExp(searchString);
      const result = _.filter(annotators, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
      return result
    },
    async refreshAnnotatorsHandler() {
      this.setLoading(true)
      await this.updateAnnotators()
      this.$emit("updated")
      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
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

  },
  watch: {
    project: {
      handler(newValue) {
        if (newValue) {
          this.updateAnnotators()
        }
      }
    }
  }
}
</script>

<style scoped>
.stageActive {
  background: #c0fdea;
}
</style>
