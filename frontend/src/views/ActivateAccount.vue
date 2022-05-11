<template>
  <div class="container">
    <h1>Activate account</h1>

    <div v-if="error || !activateSuccess">
      <p v-if="error" class="alert-warning p-4 mb-4">
        {{ error }}
      </p>

      <p v-if="reactivateMailSuccess" class="alert-success p-4 mb-4">
        The activation token has been re-sent to the e-mail address you used to
        register your account.
      </p>

      <div>
        <div class="mb-2">
          You can re-send a verification e-mail using the form below. Make sure you check your spam box.
        </div>
        <div class="form-inline">
          <b-input-group>
            <b-input name="username" v-model="reactivateUsername" placeholder="Enter username here..."></b-input>
            <b-input-group-append>
              <b-button variant="primary" @click="generateActivationCodeBtnHandler">
                Re-send verification e-mail.
              </b-button>
            </b-input-group-append>
          </b-input-group>
        </div>
      </div>
    </div>
    <div v-else>
      <p class="alert-success p-4">Thank you for activating your account.
        <span v-if="isAuthenticated">Use the navigation bar above to access the site.</span>
        <span v-else>You can <b-link to="/login">login here</b-link> to access the site.</span>
      </p>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "ActivateAccount",
  title: "Activate Account",
  data() {
    return {
      activateSuccess: false,
      error: null,
      reactivateUsername: "",
      reactivateMailSuccess: false,
    }
  },
  computed: {
    ...mapGetters(["isAuthenticated"])
  },
  methods: {
    ...mapActions(["activateAccount", "generateUserActivation"]),
    async generateActivationCodeBtnHandler() {
      try {
        let response = await this.generateUserActivation(this.reactivateUsername)
        this.reactivateMailSuccess = true
      } catch (e) {
        this.error = e.message
        this.reactivateMailSuccess = false
      }
    }
  },
  async mounted() {
    try {
      if (this.$route.query.username && this.$route.query.token) {
        let response = await this.activateAccount({
          username: this.$route.query.username,
          token: this.$route.query.token
        })
        this.activateSuccess = true
      }
    } catch (e) {
      this.error = e.message
    }


  }
}
</script>

<style scoped>

</style>
