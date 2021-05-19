<template>
  <div id="navbar">
    <div>
      <b-navbar type="dark" variant="dark">
        <b-navbar-nav>
          <b-navbar-brand to="/">GATE Annotate</b-navbar-brand>
          <b-nav-item to="/projects">Projects</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav right>
          <b-nav-item to="/login">Log In</b-nav-item>
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
