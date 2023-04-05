<template>
  <div class="home container">
    <b-row>
      <b-col>
        <div class="mt-4 text-center">
          <img src="/static/img/gate-teamware-logo.svg" alt="GATE Teamware" style="margin: auto"/>
        </div>

        <AccountActivationGenerator></AccountActivationGenerator>

      </b-col>
    </b-row>
  </div>
</template>

<script>

import AccountActivationGenerator from "@/components/AccountActivationGenerator.vue";
export default {
  name: 'Home',
  title: "GATE Teamware",
  components: {
    AccountActivationGenerator
  }
}
</script>
