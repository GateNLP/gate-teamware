<template>
  <div id="app">
    <div>
      <b-navbar type="dark" variant="dark">
        <b-navbar-nav>
          <b-nav-item to="/">Home</b-nav-item>
          <b-nav-item to="/projects">Projects</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>

          <!-- <b-nav-item-dropdown text="User" right>
            <b-dropdown-item href="#">Account</b-dropdown-item>
            <b-dropdown-item href="#">Settings</b-dropdown-item>
          </b-nav-item-dropdown> -->

        </b-navbar-nav>
      </b-navbar>
    </div>

    {{csrfToken}}
    <router-view/>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";

export default {
  computed: {
    ...mapState(["csrfToken"])
  },
  methods: {
    ...mapActions(["testrpc"])
  },
  mounted() {
    this.testrpc()
  }
}
</script>

<style>
</style>
