<template>
  <div id="navbar">
    <div>
      <b-navbar type="light" variant="light">
        <b-navbar-brand to="/">GATE Annotate</b-navbar-brand>

        <b-navbar-nav>
          <b-nav-item to="/projects" v-if="user && user.isManager && user.isActivated">Projects</b-nav-item>
          <b-nav-item to="/annotate" v-if="user && user.isAuthenticated && user.isActivated">Annotate</b-nav-item>
          <b-nav-item to="/manageusers" v-if="user && user.isAdmin && user.isActivated">Manage Users</b-nav-item>
          <b-nav-item to="/app_config" v-if="user && user.isAuthenticated && user.isActivated">Settings</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>



        <b-navbar-nav  class="ml-auto" v-if="!user || !user.isAuthenticated">
          <b-nav-item to="/login" right>Sign In</b-nav-item>
          <b-nav-item to="/register" right>Register</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav  class="ml-auto" v-else>
          <b-nav-item-dropdown right>
            <template #button-content>
              <b-icon icon="person-circle"></b-icon> {{ user.username }}
            </template>
            <b-dropdown-item to="/profile">Profile</b-dropdown-item>
            <b-dropdown-item @click="logoutHandler" right>Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
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
