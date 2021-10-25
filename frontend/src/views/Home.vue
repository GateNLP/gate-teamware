<template>
  <div class="home container">
    <h1>GATE Annotation Tool</h1>

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
