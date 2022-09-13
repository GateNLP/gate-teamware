<template>
  <b-modal v-model="showModal"
           ok-variant="danger"
           :ok-title="operationString"
           :ok-disabled="deleteLocked && deleteLocking"
           @ok="$emit('delete')"
           @hidden="deleteLocked = true"
           :title="title">

    <slot>
      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <div>
        Are you sure you want to delete?
      </div>
    </slot>

    <div v-if="deleteLocking" class="mt-4">
      <p>Press the unlock button below to enable this operation.</p>

      <b-button @click="deleteLocked = !deleteLocked"
                :class="{'btn-danger': deleteLocked, 'btn-success': !deleteLocked}"
      >
        <b-icon-lock-fill v-if="deleteLocked"></b-icon-lock-fill>
        <b-icon-unlock-fill v-else></b-icon-unlock-fill>
        <span v-if="deleteLocked">Unlock</span>
        <span v-else>Lock</span>
      </b-button>

    </div>
  </b-modal>
</template>

<script>
/**
 * Modal dialog for delete operations
 *
 * Properties
 * v-model: Shows/hides this dialog.
 * title: The title for this dialog .
 * operation-string: The text for describing the delete operation to be performed.
 * delete-locking: Should the user have to perform an extra unlock step before being able to confirm the delete.
 *
 * Events
 * delete() - Confirms the delete operation
 */
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
    },
    operationString: {
      default: "Delete"
    },
    deleteLocking: {
      default: true
    }
  }
}
</script>

<style scoped>

</style>
