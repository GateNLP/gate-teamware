<template>
  <div class="container">
    <h3>Sign In</h3>
    <b-form href="" method="post" @submit.prevent="loginHandler">

      <b-form-group label="Username">
        <b-form-input type="text" v-model="username"/>
      </b-form-group>

      <b-form-group label="Password">
        <b-form-input type="password" v-model="password"/>
      </b-form-group>

      <transition name="fade">
        <div class="alert alert-warning" role="alert" v-if="error">
          {{ error }}
        </div>
      </transition>

      <b-form-row>
        <b-col>
          <b-button type="submit" variant="primary">Sign In</b-button>
        </b-col>
      </b-form-row>
    </b-form>

    <b-row class="mt-3 small">
      <b-col>
        <b-link to="/passwordreset">Forgotten your password? Reset it here.</b-link>
      </b-col>
    </b-row>

  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";

export default {
  title: "Login",
  data() {
    return {
      error: false,
      username: null,
      password: null,
    }
  },
  methods: {
    ...mapActions(["login"]),
    async loginHandler() {
      try {
        let response = await this.login({username: this.username, password: this.password});
        if (response.isAuthenticated == true) {
          this.$router.push({name: 'Home'});
        }
      } catch (e) {
        this.error = e
      }

    }
  }
}
</script>

<style>
</style>
