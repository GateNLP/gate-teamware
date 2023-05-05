<template>
  <div id="app">
    <navbar></navbar>
    <router-view :key="$route.fullPath"></router-view>
    <pagefooter class="d-none d-md-block"></pagefooter>
  </div>
</template>
<script>
import navbar from './components/navbar.vue';
import pagefooter from './components/pagefooter.vue';
import {initToast} from "@/utils";

export default {
  components: { navbar, pagefooter },
  mounted() {
    initToast(this)
  }
}
</script>

<style>
</style>

