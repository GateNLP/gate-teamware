<template>
  <div>
    <b-collapse v-model="collapse">
      <slot></slot>
    </b-collapse>
    <a href="#" @click.prevent="collapse = !collapse">
      <span v-if="collapse">- Hide</span><span v-else>+ Show</span>
    </a>

  </div>

</template>

<script>
export default {
  name: "CollapseText",
  data() {
    return {
      collapse: false,
    }
  }
}
</script>

<style scoped>
.collapse-text {
  font-size: 14px;
  line-height: 1.5;
}

.collapse-text.collapse:not(.show) {
  display: block;
  height: 4.5em !important;
  overflow: hidden;
}

.collapse-text.collapsing {
  height: 4.5em;
}

</style>
