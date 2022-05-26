<template>
  <b-card v-if="project" class="mb-4">
    <h3>
      <ProjectIcon :project-id="project.id"></ProjectIcon>
      {{ project.name }}
    </h3>

    <DocumentsList
        :documents="documents"
        :num-total-documents="totalCount"
        :show-menu-bar="false"
        :show-filters="false"
        @fetch="fetchDocumentsHandler"

    ></DocumentsList>

  </b-card>
</template>

<script>
import {mapState, mapActions, mapGetters} from "vuex";
import DocumentsList from "@/components/DocumentsList";
import ProjectIcon from "@/components/ProjectIcon";
export default {
  name: "UserAnnotatedProject",
  components: {
    DocumentsList,
    ProjectIcon
  },
  data(){
    return {
      documents: [],
      totalCount: 0
    }
  },
  props: {
    project: {
      default: null
    }
  },
  methods: {
    ...mapActions(["getUserAnnotationsInProject"]),
    async fetchDocumentsHandler(currentPage, pageSize){
      try{
        const result = await this.getUserAnnotationsInProject(
          {
            project_id: this.project.id,
            current_page: currentPage,
            page_size: pageSize,
          })

        this.documents = result.items
        this.totalCount = result.total_count

      }catch (e){
        toastError("Could not fetch documents and annotations for project "+this.project.id, e)
      }


    }
  }
}
</script>

<style scoped>

</style>
