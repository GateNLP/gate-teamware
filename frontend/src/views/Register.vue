<template>
  <div class="container">
    <h3>Register</h3>
    <b-form href="" method="post">

      <b-form-group label="Username">
        <b-form-input type="text" v-model="form.username"/>
      </b-form-group>

      <b-form-group label="Email">
        <b-form-input type="text" v-model="form.email"/>
      </b-form-group>

      <b-form-group label="Password">
        <b-form-input type="password" v-model="form.password"/>
      </b-form-group>

      <b-form-group label="Confirm Password">
        <b-form-input type="password" v-model="form.confirmpassword" placeholder="Type password again to confirm"/>
      </b-form-group>

      <transition name="fade">
        <div class="alert alert-warning" role="alert" v-if="error">
          {{ error.message }}
        </div>
      </transition>


      <b-form-row>
        <b-col>
          <b-button variant="primary" @click="FormHandler">Register</b-button>
        </b-col>
      </b-form-row>
    </b-form>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";

export default {
  title: "Register",
  data() {
    return {
      error: null,

      form: {
        username: null,
        password: null,
        email: null,
        confirmpassword: null,
      },
    }
  },
  methods: {
    ...mapActions(["register"]),
    async FormHandler() {
      this.error = null

      try {
        if (this.form.confirmpassword != this.form.password)
          throw new Error('Password must match')

        let response = await this.register(this.form);
        this.$router.push({name: 'Home'});

      } catch (e) {
        this.error = e
      }


    }
  },

}
</script>

<style>

</style>
