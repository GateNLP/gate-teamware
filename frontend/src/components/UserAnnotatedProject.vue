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
        @fetch-annotation="refreshAnnotationHandler"
        :allow-annotation-edit="project.allow_annotation_change"
        :allow-annotation-change-delete="false"
        :project-config="project.configuration"
        ref="docsList"
    ></DocumentsList>

  </b-card>
</template>

<script>
import {mapState, mapActions, mapGetters} from "vuex";
import DocumentsList from "@/components/DocumentsList";
import ProjectIcon from "@/components/ProjectIcon";
import {toastError} from "@/utils";

export default {
  name: "UserAnnotatedProject",
  components: {
    DocumentsList,
    ProjectIcon
  },
  data() {
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
    ...mapActions(["getUserAnnotationsInProject", "getAnnotation"]),
    async fetchDocumentsHandler(currentPage, pageSize) {
      try {
        const result = await this.getUserAnnotationsInProject(
            {
              project_id: this.project.id,
              current_page: currentPage,
              page_size: pageSize,
            })

        this.documents = result.items
        this.totalCount = result.total_count

      } catch (e) {
        toastError("Could not fetch documents and annotations for project " + this.project.id, e)
      }


    },
    async refreshAnnotationHandler(annotationId) {

      try {
        const result = await this.getAnnotation(annotationId)

        function replaceDocAnnotation(vueInstance, documents) {
          for (let i = 0; i < documents.length; i++) {
            for (let j = 0; j < documents[i].annotations.length; j++) {
              if (documents[i].annotations[j].id === annotationId) {
                // Replace, alert vue that array has changed
                let doc = documents[i]
                doc.annotations[j] = result
                vueInstance.$set(documents, i, doc)
                return
              }
            }
          }
        }


        replaceDocAnnotation(this, this.documents)

        this.$emit("updated")
      } catch (e) {
        toastError("Could not reload annotation", e, this)
      }

    }
  },
  watch: {
    project: {
      handler(newProject) {
        this.$refs["docsList"].fetchDocuments()

      }
    }
  }
}
</script>

<style scoped>

</style>
