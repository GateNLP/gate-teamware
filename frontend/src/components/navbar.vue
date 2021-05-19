<template>
  <div id="navbar">
    <div>
      <b-navbar variant="light">
        <b-navbar-brand to="/">GATE Annotate</b-navbar-brand>

        <b-navbar-nav>
          <b-nav-item to="/projects">Projects</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav  class="ml-auto">
          <b-nav-item to="/login" right>Sign In</b-nav-item>
          <b-nav-item to="/register" right>Register</b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";

export default {
}
</script>

<style>
</style>
