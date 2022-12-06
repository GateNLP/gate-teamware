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

    <!-- Batch actions -->
    <div class="row">
      <b-button size="sm" @click="selectAllRows" variant="primary">
        <span aria-hidden="true"><b-icon-check-square></b-icon-check-square></span>
          Select all
      </b-button>
      <b-button size="sm" @click="clearSelected" variant="primary">
        <span aria-hidden="true"><b-icon-square></b-icon-square></span>
          Clear selected
      </b-button>

      <b-button-group>
        <b-button
            :variant="getBatchMakeAnnotatorBtnVariant(selected)"
            size="sm"
            @click="batchAllowAnnotation(selected)"
            :title="getBatchMakeAnnotatorBtnTitle(selected)"
            :disabled="getBatchMakeAnnotatorBtnDisabled(selected)"
        >
          <b-icon-pencil-square></b-icon-pencil-square>
          Make annotator
        </b-button>
        <b-button
            :variant="getBatchMakeAnnotatorActiveBtnVariant(selected)"
            size="sm"
            @click="batchMakeAnnotatorActive(selected)"
            :title="getBatchMakeAnnotatorActiveBtnTitle(selected)"
            :disabled="getBatchMakeAnnotatorActiveBtnDisabled(selected)"
        >
          <b-icon-person-check-fill></b-icon-person-check-fill>
          Make active
        </b-button>
        <b-button size="sm"
                  @click="batchRemoveAnnotator(selected)"
                  :variant="getBatchAnnotatorCompleteBtnVariant(selected)"
                  :title="getBatchAnnotatorCompleteBtnTitle(selected)"
                  :disabled="getBatchAnnotatorCompleteBtnDisabled(selected)">
          <b-icon icon="person-x-fill" aria-hidden="true"></b-icon>
          Complete
        </b-button>
        <b-button size="sm"
                  :variant="getBatchAnnotatorRejectBtnVariant(selected)"
                  :title="getBatchAnnotatorRejectBtnTitle(selected)"
                  :disabled="getBatchAnnotatorRejectBtnDisabled(selected)"
                  @click="batchRejectAnnotator(selected)">
          <b-icon-dash-circle rotate="-45"></b-icon-dash-circle>
          Reject
        </b-button>
      </b-button-group>
    </div>

    <!-- Project Annotators Table -->
    <b-table
      hover
      selectable
      select-mode="multi"
      ref="projectAnnotatorTable"
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
        <div :title="trainingTestTooltip(data, 'Training')">
          <b-icon-check-square-fill v-if="data.item.training_completed !== null"></b-icon-check-square-fill>
          <b-icon-square v-else></b-icon-square>
          {{ data.item.training_score }} / {{ project.training_documents }}
        </div>
      </template>

      <template #cell(testscoretestcompleted)="data" v-if="project.has_test_stage">
        <div :title="trainingTestTooltip(data, 'Testing')"  :class="testScoreColor(data)">
          <b-icon-check-square-fill v-if="data.item.test_completed !== null"></b-icon-check-square-fill>
          <b-icon-square v-else></b-icon-square>
          {{ data.item.test_score }} / {{ project.test_documents }}
        </div>
      </template>

      <template #cell(annotations)="data">
        <p class="text-center">{{ data.item.annotations }} / {{ project.documents }}</p>
      </template>

      <template #cell(status)="data">
        <span>{{ getAnnotatorStatus(data.item) }}</span>
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
    getMakeAnnotatorBtnVariant(annotator) {
      if(annotator.status != 0)
        return "secondary"

      if (annotator.allowed_to_annotate)
        return "secondary"
      else
        return "primary"
    },
    getBatchMakeAnnotatorBtnVariant(annotators){
      if (annotators.length < 1){
        return "secondary"
      }
      for (let annotator of annotators){
        if(annotator.status != 0)
          return "secondary"

        if (annotator.allowed_to_annotate)
          return "secondary"
      }
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
    getBatchMakeAnnotatorBtnTitle(annotators){
      if (annotators.length < 1){
        return "Select at least one user to make annotator"
      }

      for (let annotator of annotators){
        if(annotator.status != 0 || annotator.allowed_to_annotate)
          return "Invalid or redundant operation for one or more selected annotators."
      }
      return "Make selected annotators active in project."
    },
    getMakeAnnotatorBtnDisabled(annotator) {
      if(annotator.status != 0)
        return true

      if (annotator.allowed_to_annotate)
        return true
      else
        return false
    },
    getBatchMakeAnnotatorBtnDisabled(annotators){
      if (annotators.length < 1){
        return true
      }

      for (let annotator of annotators){
        if (annotator.status != 0 || annotator.allowed_to_annotate){
          return true
        }
      }
      return false
    },
    getMakeAnnotatorActiveBtnVariant(annotator){
      if(annotator.status == 0 || annotator.annotations_completed)
        return "secondary"
      else
        return "primary"

    },
    getBatchMakeAnnotatorActiveBtnVariant(annotators){
      if (annotators.length < 1){
        return "secondary"
      }
      for (let annotator of annotators){
        if(annotator.status == 0 || annotator.annotations_completed)
          return "secondary"
      }
      return "primary"
    },
    getMakeAnnotatorActiveBtnTitle(annotator){
      if(annotator.status == 0){
        return "Annotator already active in the project."
      }else if(annotator.annotations_completed){
        return "Annotations completed: " + annotator.annotations_completed
      }else
        return "Makes the annotator active in the project."

    },
    getBatchMakeAnnotatorActiveBtnTitle(annotators){
      if (annotators.length < 1){
        return "Select at least one annotator to make active"
      }

      for (let annotator of annotators){
        if(annotator.status == 0 || annotator.allowed_to_annotate)
          return "Invalid or redundant operation for one or more selected annotators."
      }
      return "Make selected annotators active in project."
    },
    getMakeAnnotatorActiveBtnDisabled(annotator){
      if (annotator.rejected){
        return false
      }else if (annotator.annotations_completed){
        return true
      }else if (annotator.status == 0){
        return true
      }else{
        return false
      }
    },
    getBatchMakeAnnotatorActiveBtnDisabled(annotators){
      if (annotators.length < 1){
        return true
      }else if (annotators.every( (annotator) => annotator.rejected)){
        return false
      }else if (annotators.every( (annotator) => annotator.annotations_completed)){
        return true
      }else if (annotators.every( (annotator) => annotator.status == 0 )){
        return true
      }else{
        return false
      }
    },
    getAnnotatorCompleteBtnVariant(annotator) {
      if(annotator.status == 0)
        return "warning"
      else
        return "secondary"

    },
    getBatchAnnotatorCompleteBtnVariant(annotators){
      if (annotators.length < 1){
        return "secondary"
      }else if (annotators.every( (annotator) => annotator.status == 0 )){
        return "warning"
      }else{
        return "secondary"
      }
    },
    getAnnotatorCompleteBtnTitle(annotator) {
      if (annotator.status == 0)
        return "Mark annotator as having completed annotation of the project and will be transferred to the available annotator pool."
      else
        return "Annotator not active in project"

    },
    getBatchAnnotatorCompleteBtnTitle(annotators){
      if (annotators.length < 1){
        return "Select at least one annotator to make active"
      }
      
      if (annotators.every( (annotator) => annotator.status == 0 )){
        return "Mark annotators as having completed annotation of the project. Annotators will be transferred to the available annotator pool."
      }else{
        return "Invalid or redundant operation for one or more selected annotators."
      }
    },
    getAnnotatorCompleteBtnDisabled(annotator) {
      return annotator.status != 0
    },
    getBatchAnnotatorCompleteBtnDisabled(annotators){
      if (annotators.length < 1){
        return true
      }else if (annotators.every( (annotator) => annotator.status == 0 )){
        return false
      }else{
        return true
      }
    },
    getAnnotatorStatus(annotator){
      if (annotator.rejected){
        return 'Rejected'
      }else if(this.isAwaitingApproval(annotator)){
        return 'Waiting'
      }else if(this.isAtTrainingStage(annotator)){
        return 'Training'
      }else if(this.isAtTestStage(annotator)){
        return 'Testing'
      }else if(this.isAtAnnotationStage(annotator)){
        return 'Annotating'
      }else if(annotator.annotations_completed){
        return 'Completed'
      }else{
        return 'Unknown'
      }
    },
    getAnnotatorRejectBtnVariant(annotator) {
      if(annotator.status == 0)
        return "danger"
      else
        return "secondary"

    },
    getBatchAnnotatorRejectBtnVariant(annotators){
      if (annotators.length < 1){
        return "secondary"
      }else if (annotators.every( (annotator) => annotator.status == 0 )){
        return "danger"
      }else{
        return "secondary"
      }
    },
    getAnnotatorRejectBtnTitle(annotator) {
      if (annotator.status == 0)
        return "Mark annotator as having rejected from annotation of the project and will be transferred to the available annotator pool."
      else
        return "Annotator not active in project"

    },
    getBatchAnnotatorRejectBtnTitle(annotators){
      if (annotators.length < 1){
        return "Select at least one annotator to make active"
      }
      
      if (annotators.every( (annotator) => annotator.status == 0 )){
        return "Mark annotators as rejected from annotation of the project. Annotators will be transferred to the available annotator pool."
      }else{
        return "Invalid or redundant operation for one or more selected annotators."
      }
    },
    getAnnotatorRejectBtnDisabled(annotator) {
      return annotator.status != 0
    },
    getBatchAnnotatorRejectBtnDisabled(annotators){
      if (annotators.length < 1){
        return true
      }else if (annotators.every( (annotator) => annotator.status == 0 )){
        return false
      }else{
        return true
      }
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
    async batchMakeAnnotatorActive(annotators){
      for (let annotator of annotators){
        this.makeAnnotatorActive(annotator.username);
      }
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
    async batchRemoveAnnotator(annotators){
      for (let annotator of annotators){
        this.removeAnnotator(annotator.username);
      }
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
    async batchRejectAnnotator(annotators){
      for (let annotator of annotators){
        this.rejectAnnotator(annotator.username);
      }
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
    async batchAllowAnnotation(annotators){
      for (let annotator of annotators){
        this.allowAnnotation(annotator.username);
      }
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
    selectAllRows() {
      this.$refs.projectAnnotatorTable.selectAllRows()
    },
    clearSelected() {
      this.$refs.projectAnnotatorTable.clearSelected()
    },
    sortBTable(aRow, bRow, key, sortDesc, formatter, compareOptions, compareLocale){
      if (key == 'usernameemail' || 'status') {
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
    testScoreColor(data){
      let test_proportion = data.item.test_score / this.project.test_documents;
      if (!data.item.test_completed){
        return "bg-transparent"
      }else if (test_proportion < this.project.min_test_pass_threshold){
        return "text-danger"
      }else if (test_proportion == test_proportion){
        return "bg-warning"
      }else{
        return "text-success"
      }
    },
    trainingTestTooltip(data, phase){
      if (phase == "Training" && data.item.training_completed){
        return "Completed: " + this.$options.filters.datetime(data.item.training_completed);
      } else if (phase == "Testing" && data.item.test_completed){

        let test_proportion = data.item.test_score / this.project.test_documents;

        let tooltip = "Completed: " + this.$options.filters.datetime(data.item.test_completed);

        if (test_proportion < this.project.min_test_pass_threshold){
            tooltip += "\nTest proportion of " + test_proportion + " below threshold of " + this.project.min_test_pass_threshold;
          }

        return tooltip

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
</style>
