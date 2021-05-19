<template>
  <div id="app">
    <navbar></navbar>
  </div>
</template>
<script>
import {mapState, mapActions} from "vuex";
import navbar from './components/navbar.vue';

export default {
  components: { navbar },
}
</script>

<style>
</style>
