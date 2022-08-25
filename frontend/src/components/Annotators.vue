<template>
  <div>
    <h2 class="mt-2 mb-2">Annotator Management
      <b-icon-question-circle id="project-annotators-help" scale="0.5"
                              style="cursor:pointer;"></b-icon-question-circle>
    </h2>
    <b-popover target="project-annotators-help" triggers="hover" placement="bottom">
      Add annotators to the project by clicking the <strong>+ Add annotators</strong> button.
      Current annotators can be managed in the table below. Removing annotators does not delete their
      completed annotations but will stop their current pending annotation task.
    </b-popover>
    <b-button-toolbar class="mt-2 mb-2">
      <b-button-group>
        <b-button :variant="loadingVariant" :disabled="loading" @click="refreshAnnotatorsHandler"
                  title="Refresh annotator list.">
          <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
          Refresh
        </b-button>
        </b-button-group>
        <b-button-group>
        <b-button :variant="loadingVariant" :disabled="loading" @click="toggleShowAddAnnotators"
                  title="Add annotators">
          + Add annotators
        </b-button>
      </b-button-group>
    </b-button-toolbar>

    <div class="row">
        <h5>Current annotators of the project</h5>
        <b-form-input v-model="projectAnnotatorSearch" placeholder="Search by username or email"></b-form-input>
        <b-pagination
          v-model="currentPageProjectAnnotators"
          :total-rows="rowsProjectAnnotators"
          :per-page="perPage"
          aria-controls="projectAnnotators"
          align="center"
        ></b-pagination>
    </div>

    <b-table
      hover
      selectable
      select-mode="multi"
      :sort-by.sync="tableSortBy"
      :sort-desc.sync="tableSortDesc"
      :sort-compare="sortBTable"
      :items="projectAnnotatorsPaginated"
      :busy="loading"
      :fields="getTableFields()"
      @row-selected="onRowSelected"
      >

      <template #cell(selected)="{ rowSelected }">
        <template v-if="rowSelected">
          <span aria-hidden="true"><b-icon-check-square></b-icon-check-square></span>
          <span class="sr-only">Selected</span>
        </template>
        <template v-else>
          <span aria-hidden="true"><b-icon-square></b-icon-square></span>
          <span class="sr-only">Not selected</span>
        </template>
      </template>

      <template #cell(usernameemail)="data">
        <span :title="data.item.email"><strong>{{ data.item.username }}</strong></span>
      </template>

      <template #cell(trainingscoretrainingcompleted)="data">
        <div :title="trainingTestTooltip(data, 'Training')" :class="{stageActive:isAtTrainingStage(data.item)}">
          <b-icon-check-square-fill v-if="data.item.training_completed !== null"></b-icon-check-square-fill>
          <b-icon-square v-else></b-icon-square>
          {{ data.item.training_score }} / {{ project.training_documents }}
        </div>
      </template>

      <template #cell(testscoretestcompleted)="data" v-if="project.has_test_stage">
        <div :title="trainingTestTooltip(data, 'Testing')" :class="{stageActive:isAtTestStage(data.item)}">
          <b-icon-check-square-fill v-if="data.item.test_completed !== null"></b-icon-check-square-fill>
          <b-icon-square v-else></b-icon-square>
          {{ data.item.test_score }} / {{ project.test_documents }}
        </div>
      </template>

      <template #cell(annotations)="data">
        {{ data.item.annotations }} / {{ project.documents }}
      </template>

      <template #cell(status)="data">
        <span v-if="data.item.rejected">Rejected</span>
        <span v-else-if="data.item.annotations_completed">Completed</span>
        <span v-else-if="isAtTrainingStage(data.item)">Training</span>
        <span v-else-if="isAtTestStage(data.item)">Testing</span>
        <span v-else-if="isAtAnnotationStage(data.item)">Annotating</span>
        <span v-else-if="isAwaitingApproval(data.item)" title="Awaiting approval to annotate">Waiting</span>
        <span v-else>Unknown</span>
      </template>

      <!-- Actions -->
      <template #cell(username)="data">

        <b-button-group>
          <b-button
              :variant="getMakeAnnotatorBtnVariant(data.item)"
              size="sm"
              @click="allowAnnotation(data.value)"
              :title="getMakeAnnotatorBtnTitle(data.item)"
              :disabled="getMakeAnnotatorBtnDisabled(data.item)"
          >
            <b-icon-pencil-square></b-icon-pencil-square>
            Make annotator
          </b-button>
          <b-button
              :variant="getMakeAnnotatorActiveBtnVariant(data.item)"
              size="sm"
              @click="makeAnnotatorActive(data.value)"
              :title="getMakeAnnotatorActiveBtnTitle(data.item)"
              :disabled="getMakeAnnotatorActiveBtnDisabled(data.item)"
          >
            <b-icon-person-check-fill></b-icon-person-check-fill>
            Make active
          </b-button>
          <b-button size="sm"
                    @click="removeAnnotator(data.value)"
                    :variant="getAnnotatorCompleteBtnVariant(data.item)"

                    :title="getAnnotatorCompleteBtnTitle(data.item)"
                    :disabled="getAnnotatorCompleteBtnDisabled(data.item)">
            <b-icon icon="person-x-fill" aria-hidden="true"></b-icon>
            Complete
          </b-button>
          <b-button size="sm"
                    :variant="getAnnotatorRejectBtnVariant(data.item)"
                    :title="getAnnotatorRejectBtnTitle(data.item)"
                    :disabled="getAnnotatorRejectBtnDisabled(data.item)"
                    @click="rejectAnnotator(data.value)">
            <b-icon-dash-circle rotate="-45"></b-icon-dash-circle>
            Reject
          </b-button>
        </b-button-group>
      </template>
    
    </b-table>


      <!-- Modal - Add Annotators -->
      <b-modal class="col-6" v-model="showAddAnnotators">
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

      </b-modal>
  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import {toastError} from "@/utils";

export default {
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
      showAddAnnotators: false,
      tableSortBy: 'usernameemail',
      tableSortDesc: false,
      defaultTableFields: [
        'selected',
        {key:'usernameemail', label: 'User', sortable: true},
        {key: 'annotations', label: '# Annotations', sortable: true},
        {key: 'status', label: 'Status', sortable: true},
        {key: 'username', label: 'Actions'}
      ],
      optionalTableFields: {
        training: {key:'trainingscoretrainingcompleted', label: "Training", sortable: true},
        test: {key:'testscoretestcompleted', label: "Test", sortable: true},
      },
      selected: []  
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
      "projectAnnotatorAllowAnnotation", "rejectProjectAnnotator", "makeProjectAnnotatorActive"]),

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
    isAwaitingApproval(annotator){
      if (annotator.status == 1 || annotator.rejected || annotator.allowed_to_annotate){
        return false
      }else if(!this.project.has_training_stage && !this.project.has_test_stage){
        return false
      }else if(this.project.has_training_stage && this.project.has_test_stage){
        if (annotator.training_completed && annotator.test_completed && !annotator.allowed_to_annotate){
          return true
        }else{
          return false
        }
      }else if(this.project.has_training_stage && !this.project.has_test_stage){
        if (annotator.training_completed && !annotator.allowed_to_annotate){
          return true
        }else{
          return false
        }
      }else if(!this.project.has_training_stage && this.project.has_test_stage){
        if (annotator.test_completed && !annotator.allowed_to_annotate){
          return true
        }else{
          return false
        }
      }
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
    getAnnotationStageBackgroundClass(annotator){
      if(this.isAtAnnotationStage(annotator)){
        return {stageActive: true}
      }
      else if(this.getAnnotationStageWarning(annotator)){
        return {stageWarning: true}
      }

      return {}
    },
    getMakeAnnotatorBtnVariant(annotator) {
      if(annotator.status != 0)
        return "secondary"

      if (annotator.allowed_to_annotate)
        return "secondary"
      else
        return "primary"
    },
    getMakeAnnotatorBtnTitle(annotator) {
      if(annotator.status != 0)
        return "Annotator is not active in this project."

      if (annotator.allowed_to_annotate)
        return "Annotator already allowed to annotate."
      else
        return "Allow annotator to annotate data. Training and testing stages are skipped if not already completed."

    },
    getMakeAnnotatorBtnDisabled(annotator) {
      if(annotator.status != 0)
        return true

      if (annotator.allowed_to_annotate)
        return true
      else
        return false
    },
    getMakeAnnotatorActiveBtnVariant(annotator){
      if(annotator.status == 0)
        return "secondary"
      else
        return "primary"

    },
    getMakeAnnotatorActiveBtnTitle(annotator){
      if(annotator.status == 0)
        return "Annotator already active in the project."
      else
        return "Makes the annotator active in the project."

    },
    getMakeAnnotatorActiveBtnDisabled(annotator){
      return annotator.status == 0

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
      try {
        await this.addProjectAnnotator({projectID: this.project.id, username: username});
        await this.updateAnnotators();
        this.$emit("updated")
      } catch (e) {
        toastError("Could not add annotator", e, this)
      }

      this.setLoading(false)
    },
    async makeAnnotatorActive(username) {
      this.setLoading(true)
      try {
        await this.makeProjectAnnotatorActive({projectID: this.project.id, username: username});
        await this.updateAnnotators();
        this.$emit("updated")
      } catch (e) {
        toastError("Could not make annotator active", e, this)
      }

      this.setLoading(false)
    },
    async removeAnnotator(username) {
      this.setLoading(true)

      try {
        await this.removeProjectAnnotator({projectID: this.project.id, username: username});
        await this.updateAnnotators();
        this.$emit("updated")
      } catch (e) {
        toastError("Could not remove annotator", e, this)
      }

      this.setLoading(false)
    },
    async rejectAnnotator(username) {
      this.setLoading(true)
      try {
        await this.rejectProjectAnnotator({projectID: this.project.id, username: username});
        await this.updateAnnotators();
        this.$emit("updated")

      } catch (e) {
        toastError("Could not reject annotator", e, this)
      }

      this.setLoading(false)
    },
    async allowAnnotation(username) {
      this.setLoading(true)
      try {
        await this.projectAnnotatorAllowAnnotation({projectID: this.project.id, username: username});
        await this.updateAnnotators();
        this.$emit("updated")
      } catch (e) {
        toastError("Could not make this user an annotator", e, this)
      }

      this.setLoading(false)
    },
    searchAnnotators(annotators, searchString) {
      const regEx = new RegExp(searchString);
      const result = _.filter(annotators, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
      return result
    },
    async refreshAnnotatorsHandler() {
      this.setLoading(true)
      try {
        await this.updateAnnotators()
        this.$emit("updated")
      } catch (e) {
        toastError("Could not update annotator list", e, this)
      }

      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
    toggleShowAddAnnotators(){
      this.showAddAnnotators = !this.showAddAnnotators;
    },
    onRowSelected(items){
      this.selected = items;
    },
    getTableFields(){
      let fields =  JSON.parse(JSON.stringify(this.defaultTableFields));
      if (this.project.has_test_stage) {
        fields.splice(2,0,this.optionalTableFields.test)
      }
      if (this.project.has_training_stage) {
        fields.splice(2,0,this.optionalTableFields.training)
      }
      return fields
    },
    sortBTable(aRow, bRow, key, sortDesc, formatter, compareOptions, compareLocale){
      if (key == 'usernameemail' || 'sorted') {
        const a = aRow.username
        const b = bRow.username
        return a.localeCompare(b, compareLocale, compareOptions)
      }else if(key == 'trainingscoretrainingcompleted'){
        const a = aRow.training_score
        const b = bRow.training_score
        return a < b ? -1 : a > b ? 1 : 0 
      }else if(key == 'testscoretestcompleted'){
        const a = aRow.test_score
        const b = bRow.test_score
        return a < b ? -1 : a > b ? 1 : 0
      }else if(key == 'annotations'){
        const a = aRow.annotations
        const b = bRow.annotations
        return a < b ? -1 : a > b ? 1 : 0 
      }else{
        return null // fall back to built-in sort-compare fcn
      }
    },
    trainingTestTooltip(data, phase){
      if (phase == "Training" && data.item.training_completed){
        return "Completed: " + this.$options.filters.datetime(data.item.training_completed);
      } else if (phase == "Testing" && data.item.test_completed){
        return "Completed: " + this.$options.filters.datetime(data.item.test_completed);
      } else if (phase == "Testing" && !data.item.training_completed && this.project.has_training_stage){
        return "Testing not started"
      } else {
        return phase + " in progress"
      }
    }
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
.stageWarning {
  background: #fac980;
}
</style>
