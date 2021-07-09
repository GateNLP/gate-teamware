<template>
  <div id="navbar">
    <div>
      <b-navbar variant="light">
        <b-navbar-brand to="/">GATE Annotate</b-navbar-brand>

        <b-navbar-nav>
          <b-nav-item to="/projects" v-if="user && user.isAuthenticated">Projects</b-nav-item>
          <b-nav-item to="/annotate" v-if="user && user.isAuthenticated">Annotate</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>



        <b-navbar-nav  class="ml-auto" v-if="!user || !user.isAuthenticated">
          <b-nav-item to="/login" right>Sign In</b-nav-item>
          <b-nav-item to="/register" right>Register</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav  class="ml-auto" v-else>
          <b-nav-text variant="dark">Logged in as: {{ user.username }}</b-nav-text>
          <b-nav-item @click="logoutHandler" right>Sign Out</b-nav-item>
        </b-navbar-nav>

      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";

export default {
    computed:{
        ...mapState(["user"]),
    },
    methods:{
      ...mapActions(["logout"]),
      logoutHandler(){
        this.logout();
        this.$router.push({ name: 'Home' });
      },
    },
}
</script>

<style>
</style>
