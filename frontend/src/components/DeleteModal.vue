<template>
  <b-modal v-model="showModal"
           ok-variant="danger"
           ok-title="Delete"
           :ok-disabled="deleteLocked"
           @ok="$emit('delete')"
           @hidden="deleteLocked = true"
           :title="title">

    <slot>
      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <div>
        Are you sure you want to delete?
      </div>
    </slot>

    <div>
      <b-button @click="deleteLocked = !deleteLocked"
                :class="{'btn-danger': deleteLocked, 'btn-success': !deleteLocked}"
      >
        <b-icon-lock-fill v-if="deleteLocked"></b-icon-lock-fill>
        <b-icon-unlock-fill v-else></b-icon-unlock-fill>
        <span v-if="deleteLocked">Unlock delete</span>
        <span v-else>Lock delete</span>
      </b-button>

    </div>
  </b-modal>
</template>

<script>
export default {
  name: "DeleteModal",
  data() {
    return {
      deleteLocked: true,
    }
  },
  computed: {
    showModal:{
      get(){
        return this.value
      },
      set(newValue){
        this.$emit("input", newValue)
      }
    }
  },
  props: {
    value: {
      default: false
    },
    title: {
      default: "Confirm delete"
    }
  }
}
</script>

<style scoped>

</style>
