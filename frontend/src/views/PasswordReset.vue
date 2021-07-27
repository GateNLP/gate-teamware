<template>
  <div class="container">
    <h1>Password reset</h1>
    <b-row v-if="this.$route.query.username && this.$route.query.token">
      <b-col md="6">
        <b-form v-if="!resetSuccess">
          <p>Please provide a new password.</p>
          <b-form-group label="Password">
            <b-input type="password"  name="password"  v-model="newPassword"></b-input>
          </b-form-group>
          <b-form-group label="Confirm new password">
            <b-input type="password" name="passwordConfirm"  v-model="newPasswordConfirm"></b-input>
          </b-form-group>
          <b-input-group>
            <b-button variant="primary" @click="resetPasswordBtnHandler">Reset password</b-button>
          </b-input-group>

        </b-form>

        <p v-if="resetSuccess" class="alert-success p-4 mb-4 mt-3">
          Your password has been reset.
        </p>

        <p v-if="resetError" class="alert-warning p-4 mb-4 mt-3">
          {{ resetError }}
        </p>

      </b-col>
    </b-row>
    <b-row v-else>
      <b-col md="6">
        <b-form>
          <p>Send a password reset email by providing your username below...</p>
          <b-input-group>
            <b-input name="username" placeholder="Username..." v-model="username"></b-input>
            <b-input-group-append>
              <b-button variant="primary" @click="generateResetPasswordBtnHandler">Reset password</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form>

        <p v-if="generateSuccess" class="alert-success p-4 mb-4 mt-3">
          The activation token has been re-sent to the e-mail address you used to
          register your account.
        </p>

        <p v-if="generateError" class="alert-warning p-4 mb-4 mt-3">
          {{ generateError }}
        </p>

      </b-col>
    </b-row>




  </div>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "PasswordReset",
  data() {
    return {
      username: "",
      generateSuccess: false,
      generateError: null,
      newPassword: "",
      newPasswordConfirm: "",
      resetSuccess: false,
      resetError: null,

    }
  },
  methods: {
    ...mapActions(["resetPassword", "generatePasswordReset"]),
    async generateResetPasswordBtnHandler() {
      try {
        await this.generatePasswordReset(this.username)
        this.generateSuccess = true
        this.generateError = null

      } catch (e) {
        this.generateSuccess = false
        this.generateError = e.message
      }

    },
    async resetPasswordBtnHandler(){
      try {

        if(this.newPassword !== this.newPasswordConfirm)
          throw new Error("Password must match")

        await this.resetPassword({
          username: this.$route.query.username,
          token: this.$route.query.token,
          newPassword: this.newPassword
        })
        this.resetSuccess = true
        this.resetError = null

      } catch (e) {
        console.log(e)

        this.resetSuccess = false
        this.resetError = e.message
      }

    }

  },
}
</script>

<style scoped>

</style>
