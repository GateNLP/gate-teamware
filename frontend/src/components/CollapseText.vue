<template>
  <div>
    <div ref="collapse-container" :class="collapseClass">
      <div v-if="collapse" class="collapse-overlay"></div>
      <slot></slot>
    </div>
    <a href="#" @click.prevent="collapse = !collapse">
      <span v-if="collapse">+ Show</span><span v-else>- Hide</span>
    </a>
  </div>
</template>

<script>
export default {
  name: "CollapseText",
  data() {
    return {
      collapse: true,
    }
  },
  computed: {
    collapseClass(){
      return {
        "collapse-text": this.collapse,
        "expand-text": !this.collapse
      }
    }
  },
}
</script>

<style scoped>


.collapse-text {
  position: relative;
  height: 5rem;
  overflow: hidden;

}

.expand-text {
  position: relative;
  height: auto;
  overflow: hidden;

}

.collapse-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background: linear-gradient(rgba(255, 255, 255, 0) 70%, rgba(255, 255, 255, 255));
}



</style>
