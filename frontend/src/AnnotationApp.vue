<template>
  <div id="app">
    <navbar></navbar>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";
import navbar from './components/navbar.vue';
import Cookies from 'js-cookie'

export default {
  components: { navbar },
  methods: {
    ...mapActions(["updateUser"]),
  },
  mounted() {
    //Checks for user cookie
    const username = Cookies.get('username')
    if (username) {
        this.updateUser({username: username, isAuthenticated: true});
    }
  },
}
</script>

<style>
</style>
