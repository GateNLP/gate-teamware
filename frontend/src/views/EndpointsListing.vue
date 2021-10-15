<template>
  <div class="container">

    <h1>Endpoints</h1>

    <b-row class="font-weight-bold">
      <b-col>Function name</b-col>
      <b-col>Parameters</b-col>
      <b-col>Permission</b-col>
      <b-col>Description</b-col>
    </b-row>

    <b-row v-for="(spec, name) in endpoints" :key="name" class="mb-2 mt-2 pt-1 pb-1 border-bottom">
      <b-col>
        <strong>{{name}}</strong>
      </b-col>
      <b-col>
        <span class="badge badge-info mr-2" v-for="argname in spec.arguments" :key="argname">
          {{argname}}
        </span>
      </b-col>
      <b-col >
        <b-badge variant="danger" v-if="spec.require_admin" class="mr-2">Admin</b-badge>
        <b-badge variant="warning" v-else-if="spec.require_manager" class="mr-2">Manager</b-badge>
        <b-badge variant="primary" v-else-if="spec.require_authentication" class="mr-2">Annotator</b-badge>
      </b-col>
      <b-col>
        <p v-html="spec.description"></p>

      </b-col>


    </b-row>

  </div>

</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "EndpointsListing",
  data(){
    return {
      endpoints: {}
    }

  },
  methods:{
    ...mapActions(["getEndpointListing"]),

  },
  async mounted() {
    this.endpoints = await this.getEndpointListing()

  }

}
</script>

<style scoped>

</style>
