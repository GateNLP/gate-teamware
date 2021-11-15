<template>
  <div class="home container">
    <div class="mt-4 text-center">
      <img src="/static/img/gate-teamware-logo.svg" alt="GATE Teamware" style="margin: auto"/>
    </div>


    <AccountActivationGenerator></AccountActivationGenerator>
  </div>
</template>

<script>

import AccountActivationGenerator from "@/components/AccountActivationGenerator";
export default {
  name: 'Home',
  title: "Gate Annotation Service",
  components: {
    AccountActivationGenerator
  }
}
</script>
