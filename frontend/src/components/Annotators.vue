<template>
  <div class="container">
    <div class="row">
      <div class="col-6">
        <h5>Current annotators of the project</h5>

        <b-list-group>
          <b-list-group-item href="#" v-for="annotator in projectAnnotators" v-bind:key="annotator.id"
            @click="removeAnnotator(annotator.username)">
            <b-icon icon="person-x-fill" aria-hidden="true" variant="danger"></b-icon>
            {{ annotator.username }}
          </b-list-group-item>
        </b-list-group>

      </div>
      <div class="col-6">
        <h5>Add annotator to project</h5>

        <b-list-group>
          <b-list-group-item href="#" v-for="annotator in possibleAnnotators" v-bind:key="annotator.id"
            @click="addAnnotator(annotator.username)">
            <b-icon icon="person-plus-fill" aria-hidden="true" variant="success"></b-icon>
            {{ annotator.username }}
          </b-list-group-item>
        </b-list-group>


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
      projectAnnotators: [],
    }
  },
  props:{
    projectID: {
      type: String,
      default: null,
    }
  },
  computed: {
    ...mapState(["projects"]),
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
    }
  },
  mounted(){
    this.updateAnnotators();
  }
}
</script>

<style scoped>

</style>