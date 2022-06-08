<template>
  <div>
    <b-badge variant="success" class="mr-2" title="Completed annotations">
      <b-icon-pencil-fill></b-icon-pencil-fill>
      {{ project.completed_tasks }}
    </b-badge>
    <b-badge variant="danger" class="mr-2" title="Rejected annotations">
      <b-icon-x-square-fill></b-icon-x-square-fill>
      {{ project.rejected_tasks }}
    </b-badge>
    <b-badge variant="warning" class="mr-2" title="Timed out annotations">
      <b-icon-clock></b-icon-clock>
      {{ project.timed_out_tasks }}
    </b-badge>
    <b-badge variant="secondary" class="mr-2" title="Aborted annotations">
      <b-icon-stop-fill></b-icon-stop-fill>
      {{ project.aborted_tasks }}
    </b-badge>
    <b-badge variant="primary" class="mr-2" title="Pending annotations">
      <b-icon-play-fill></b-icon-play-fill>
      {{ project.pending_tasks }}
    </b-badge>
    <b-badge variant="dark" class="mr-2" title="Occupied (completed & pending)/Total tasks">
      <b-icon-card-checklist></b-icon-card-checklist>
      {{ project.completed_tasks + project.pending_tasks }}/{{ project.total_tasks }}
    </b-badge>
    <b-badge variant="info" class="mr-2" title="Number of documents/ training documents/ test documents">
      <b-icon-file-earmark-fill></b-icon-file-earmark-fill>
      {{ project.documents }}/{{ project.training_documents }}/{{ project.test_documents }}
    </b-badge>
    <b-badge variant="primary" class="mr-2"
             title="Number of current annotators. Annotators are removed from the project when they have completed all annotation tasks in their quota.">
      <b-icon-person-fill></b-icon-person-fill>
      {{ project.num_annotators }}
    </b-badge>

  </div>

</template>

<script>
export default {
  name: "ProjectStatusBadges",
  props: {
    project: {
      default() {
        return {}
      }
    }
  }
}
</script>

<style scoped>

</style>
