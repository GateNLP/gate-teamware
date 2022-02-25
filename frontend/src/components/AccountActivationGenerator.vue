<template>
  <b-row class="mt-3" v-if="!isActivated && isAuthenticated">
    <b-col>
      <p class="alert-warning p-2">
        Your account must be activated before you can use the website. If you have not received the
        activation e-mail, you can re-generate it using the button below.
      </p>
      <div>
        <b-button variant="primary" @click="generateActivationCodeBtnHandler">
          Re-send verification e-mail.
        </b-button>

      </div>
    </b-col>

  </b-row>

</template>

<script>
import {mapActions, mapGetters} from "vuex";
import {toastError, toastSuccess} from "@/utils";

export default {
  name: "AccountActivationGenerator",
  computed: {
    ...mapGetters(["isActivated", "isAuthenticated", "username"]),
  },
  methods: {
    ...mapActions(["generateUserActivation"]),
    async generateActivationCodeBtnHandler() {
      try {
        await this.generateUserActivation(this.username)
        toastSuccess("Generate activation code", "Account activation code has been sent to your e-mail.", this)

      } catch (e) {
        toastError("Could not generate activation code", e, this)
      }

    },
  }
}
</script>

<style scoped>

</style>
