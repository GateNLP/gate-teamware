<template>
  <div id="app">
    <navbar></navbar>
  </div>
</template>
<script>
import navbar from './components/navbar.vue';
import {initToast} from "@/utils";

export default {
  components: { navbar },
  mounted() {
    initToast(this)
  }
}
</script>

<style>
</style>

