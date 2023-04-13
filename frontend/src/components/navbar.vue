<template>
  <div id="navbar">
    <div>
      <b-navbar type="light" variant="light" toggleable="md">
        <b-navbar-brand to="/">
          <div style="display: flex; align-content: center">
            <div class="mr-1"><img src="/static/img/GATEName.svg" alt="GATE" style="height: 1em; width: auto;"/></div>
            <div style="font-size: 1.2em ;color: #e60000">TEAMWARE</div>
          </div>
        </b-navbar-brand>

        <b-navbar-toggle target="navbar-collapse"></b-navbar-toggle>

        <b-collapse id="navbar-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/projects" v-if="user && (user.isManager || user.isAdmin) && user.isActivated">Projects
            </b-nav-item>
            <b-nav-item to="/annotate" v-if="user && user.isAuthenticated && user.isActivated">Annotate</b-nav-item>
            <b-nav-item to="/manageusers" v-if="user && user.isAdmin && user.isActivated">Manage Users</b-nav-item>
            <b-nav-item target="_blank"
                        href="https://github.com/GateNLP/gate-teamware/issues/new/choose">
              Report bugs
              <b-icon-box-arrow-up-right
                  style="position: relative; font-size: 0.8em; padding-bottom: 0.2em;"></b-icon-box-arrow-up-right>
            </b-nav-item>
            <b-nav-item target="_blank" href="https://gatenlp.github.io/gate-teamware/"> Documentation
              <b-icon-box-arrow-up-right
                  style="position: relative; font-size: 0.8em; padding-bottom: 0.2em;"></b-icon-box-arrow-up-right>
            </b-nav-item>
          </b-navbar-nav>

          <!-- Footer content to display in navbar menu on smaller screens -->
          <b-navbar-nav class="d-block d-md-none" small="true">
            <b-nav-item href="https://github.com/GATENLP/gate-teamware" target="_blank">
              Source Code
              <b-icon-box-arrow-up-right
              style="position: relative; font-size: 0.8em; padding-bottom: 0.2em;"></b-icon-box-arrow-up-right>
            </b-nav-item>
            <b-nav-item to="/privacypolicy">Privacy Policy</b-nav-item>
            <b-nav-item to="/cookies">Cookies Policy</b-nav-item>
            <b-nav-item to="/terms">Terms & Conditions</b-nav-item>
            <b-nav-item to="/about">About</b-nav-item>
            <b-nav-text>v{{ appVersion }}</b-nav-text>
          </b-navbar-nav>


          <b-navbar-nav class="ml-auto" v-if="!user || !user.isAuthenticated">
            <b-nav-item to="/login" right>Sign In</b-nav-item>
            <b-nav-item to="/register" right>Register</b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto" v-else>
            <b-nav-item-dropdown right class="user-profile-menu">
              <template #button-content>
                <b-icon icon="person-circle"></b-icon>
                {{ user.username }}
              </template>
              <b-dropdown-item to="/account">Account</b-dropdown-item>
              <b-dropdown-item to="/user_annotations">My annotations</b-dropdown-item>
              <b-dropdown-item @click="logoutHandler" right>Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>

        </b-collapse>


      </b-navbar>
    </div>

  </div>
</template>
<script>
import {mapState, mapActions, mapGetters} from "vuex";
import {version} from '../../../package.json'

export default {
  data: () => ({
    appVersion: version
  }),
  computed: {
    ...mapState(["user"]),
  },
  methods: {
    ...mapActions(["logout"]),
    logoutHandler() {
      this.logout();
      this.$router.push({name: 'Home'}).catch(() => {
      });
    },
  },
}
</script>

<style>
</style>
