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
    <img src="@/assets/logo.png"/>
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
