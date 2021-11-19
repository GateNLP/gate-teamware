<template>
  <div class="container pt-2">
    <h1>
      <ProjectIcon :project-id="projectId"></ProjectIcon>
      {{ local_project.name }}
    </h1>

    <b-card class="mt-2 mb-2">
      <h4>Project overview</h4>
      <p class="form-text text-muted">
        Current status of the project.
      </p>
      <ProjectStatusBadges :project="local_project"></ProjectStatusBadges>


      <div v-if="!local_project.is_configured" class="alert alert-warning mt-2" >
        <b-icon-exclamation-triangle></b-icon-exclamation-triangle>
        Improperly configured project:
        <ul>
          <li v-for="message in local_project.configuration_error">{{ message }}</li>
        </ul>
      </div>
      <div v-else-if="local_project.is_completed" class="alert alert-success mt-2" >
        <b-icon-check-square></b-icon-check-square> All annotation tasks in this project are completed.
      </div>

    </b-card>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">

        <h2 class="mt-2 mb-2">Project configuration
          <b-icon-question-circle id="project-config-help" scale="0.5" style="cursor:pointer;"></b-icon-question-circle>
        </h2>
        <b-popover target="project-config-help" triggers="hover" placement="bottom">
          The project can be configured in this tab with name, description and how annotations are captured.
          Once you've configured the project, don't forget to <strong>save the project configuration</strong>.
          Documents &amp; annotations can be added and managed on the <a href="#" @click.prevent="activeTab = 1">Documents
          &amp; Annotations</a> page.
          Annotators can be recruited by using the <a href="#" @click.prevent="activeTab = 2">Annotators</a> page.
        </b-popover>

        <b-button-toolbar class="mt-2 mb-2">
          <b-button-group>
            <b-button @click="saveProjectHandler" :variant="loadingVariant" :disabled="loading"
                      title="Save project configuration.">
              <b-icon-box-arrow-in-down :animation="loadingIconAnimation"></b-icon-box-arrow-in-down>
              Save
            </b-button>
            <b-button @click="$refs.projectConfigImportInput.click()" :variant="loadingVariant" :disabled="loading"
                      title="Import JSON project configuration file.">
              <b-icon-cloud-upload :animation="loadingIconAnimation"></b-icon-cloud-upload>
              Import
            </b-button>
            <b-button @click="exportProjectConfigHandler" :variant="loadingVariant" :disabled="loading"
                      title="Export project configuration as a JSON file.">
              <b-icon-cloud-download :animation="loadingIconAnimation"></b-icon-cloud-download>
              Export
            </b-button>
            <b-button @click="cloneProjectConfigHandler" :variant="loadingVariant" :disabled="loading"
                      title="Create a new project using this project's configuration. Does not copy documents, annotations or annotator list.">
              <b-icon-clipboard :animation="loadingIconAnimation"></b-icon-clipboard>
              Clone this project
            </b-button>


          </b-button-group>
        </b-button-toolbar>

        <input ref="projectConfigImportInput" type="file" accept=".json" @change="importProjectConfigHandler" hidden/>

        <b-form class="mt-4 mb-4">
          <b-form-group label="Name" description="The name of this annotation project.">
            <b-form-input v-model="local_project.name" name="project_name"></b-form-input>
          </b-form-group>
          <b-form-group label="Description"
                        description="The description of this annotation project that will be shown to annotators. Supports markdown and HTML.">
            <MarkdownEditor v-model="local_project.description"></MarkdownEditor>
          </b-form-group>
          <b-form-group label="Annotator guideline"
                        description="The description of this annotation project that will be shown to annotators. Supports markdown and HTML.">
            <MarkdownEditor v-model="local_project.annotator_guideline"></MarkdownEditor>
          </b-form-group>
          <b-form-group label="Annotations per document"
                        description="The project completes when each document in this annotation project have this many number of valid annotations. When a project completes, all project annotators will be un-recruited and be allowed to annotate other projects.">
            <b-form-input v-model="local_project.annotations_per_doc"></b-form-input>
          </b-form-group>
          <b-form-group label="Maximum proportion of documents annotated per annotator (between 0 and 1)"
                        description="A single annotator cannot annotate more than this proportion of documents.">
            <b-form-input v-model="local_project.annotator_max_annotation"></b-form-input>
          </b-form-group>
          <b-form-group label="Timeout for pending annotation tasks (minutes)"
                        description="Specify the number of minutes a user has to complete an annotation task (i.e. annotating a single document).">
            <b-form-input v-model="local_project.annotation_timeout"></b-form-input>
          </b-form-group>
          <b-form-group label="Reject documents"
                        description="Switching this off will mean that annotators for this project will be unable to choose to reject documents.">
                <b-form-checkbox
                  id="reject-checkbox"
                  v-model="local_project.allow_document_reject"
                  name="reject-checkbox"
                  switch
                >
                  Allow annotators to reject documents?
                </b-form-checkbox>
          </b-form-group>
          <b-form-group label="Document ID field"
                        description="The field in your uploaded documents that is used as a unique identifier. GATE's json format uses the name field. You can use a dot limited key path to access subfields e.g. enter features.name to get the id from the object {'features':{'name':'nameValue'}}">
            <b-form-input v-model="local_project.document_id_field"></b-form-input>
          </b-form-group>
          <b-form-row>
            <b-col>
              <h4 id="annotation-preview">Annotation configuration</h4>
              <p class="form-text text-muted">Configure how the project will capture annotations below. The
                configuration
                is in JSON format, you must provide a list of widgets to use for displaying information or capturing
                annotations.
                See the <a target="_blank"
                           href="https://gatenlp.github.io/gate-teamware/userguide/projectconfig.html">documentation
                  page on configuring project annotation</a>
                for more details.</p>
              <JsonEditor v-model="local_project.configuration" data-cy="editor"></JsonEditor>
            </b-col>
            <b-col>
              <h4>Annotation preview</h4>
              <p class="form-text text-muted">A live preview of what annotators will see according to the annotation
                configuration. You can use this to test the
                behaviour of the annotation widgets. Press <strong>Submit</strong> to check validation behaviour. Output
                of the annotation
                is shown in the <a href="#annotation-output-preview">Annotation output preview</a> below.</p>
              <b-card>
                <AnnotationRenderer :config="local_project.configuration"
                                    :document="local_project.document_input_preview"
                                    @input="annotationOutputHandler"></AnnotationRenderer>

              </b-card>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <h5 class="mt-4" id="document-input-preview">Document input preview</h5>
              <p class="form-text text-muted">An example of a document in JSON. You can modify the contents below to see
                how your
                document looks in the <a href="#annotation-preview">Annotation Preview</a>.</p>
              <VJsoneditor v-model="local_project.document_input_preview" :options="{mode: 'code'}" :plus="false"
                           height="400px"></VJsoneditor>
            </b-col>
            <b-col>
              <h5 class="mt-4" id="annotation-output-preview">Annotation output preview</h5>
              <p class="form-text text-muted">
                Live preview of the JSON annotation output after performing annotation in the <a
                  href="#annotation-preview">Annotation preview</a>.
              </p>
              <VJsoneditor v-model="annotationOutput" :options="{mode: 'preview', mainMenuBar: false}" :plus="false"
                           height="400px"></VJsoneditor>
            </b-col>
          </b-form-row>

        </b-form>
      </b-tab>

      <b-tab title="Documents & Annotations">
        <h2 class="mt-2 mb-2">Documents & Annotations
          <b-icon-question-circle id="project-documents-help" scale="0.5"
                                  style="cursor:pointer;"></b-icon-question-circle>
        </h2>
        <b-popover target="project-documents-help" triggers="hover" placement="bottom">
          You can view the list of documents and annotations of this project in this tab.
          Start by <a href="#" @click.prevent="uploadBtnHandler">uploading</a> documents to the project,
          documents must be in a JSON format. Annotators can then be recruited by using the <a href="#"
                                                                                               @click.prevent="activeTab = 2">Annotators</a>
          page.

        </b-popover>

        <b-button-toolbar class="mt-2 mb-2">
          <b-button-group>
            <b-button v-if="isEverythingSelected()"
                      :title="'Clear selection. (' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations selected)'"
                      @click="$refs.docsList.clearDocumentSelection()">
              <b-icon-check-square></b-icon-check-square>
              <span style="width: 30px">&nbsp;</span>
              {{ selectedDocuments.length }}
              <b-icon-file-earmark-text></b-icon-file-earmark-text>
              {{ selectedAnnotations.length }}
              <b-icon-pencil-square></b-icon-pencil-square>
            </b-button>
            <b-button v-else
                      :title="'Select all (' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations selected)'"
                      @click="$refs.docsList.selectAllDocuments()">
              <b-icon-square></b-icon-square>
              <span style="width: 30px">&nbsp;</span>
              <span style="width: 3em">&nbsp;</span>
              {{ selectedDocuments.length }}
              <b-icon-file-earmark-text></b-icon-file-earmark-text>
              {{ selectedAnnotations.length }}
              <b-icon-pencil-square></b-icon-pencil-square>
            </b-button>
            <b-dropdown>
              <b-dropdown-item @click="$refs.docsList.selectAllAnnotations()">
                Select all annotations
              </b-dropdown-item>
              <b-dropdown-item @click="$refs.docsList.clearAnnotationSelection()">
                Clear all annotations
              </b-dropdown-item>
            </b-dropdown>
            <b-button variant="danger" @click="showDeleteConfirmModal = !showDeleteConfirmModal"
                      :disabled="selectedDocuments.length < 1 && selectedAnnotations.length < 1"
                      :title="'Delete ' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations.'">
              <b-icon-trash-fill scale="1"></b-icon-trash-fill>
              Delete
            </b-button>
            <b-button :variant="loadingVariant" :disabled="loading" @click="refreshDocumentsHandler">
              <b-icon-arrow-clockwise :animation="loadingIconAnimation"></b-icon-arrow-clockwise>
              Refresh
            </b-button>
            <b-button variant="primary" @click="showDocumentUploadModal = true" title="Upload documents">
              <b-icon-upload></b-icon-upload>
              Upload
            </b-button>
            <b-button @click="showDocumentExportModal = true" variant="primary">
                  <b-icon-download></b-icon-download>
                  Export
            </b-button>
          </b-button-group>


        </b-button-toolbar>

        <DocumentUploader v-model="showDocumentUploadModal"
                          :project-id="projectId"
                          @uploading="documentStartUploadHandler"
                          @completed="documentUploadHandler"></DocumentUploader>

        <DocumentExporter v-model="showDocumentExportModal"
                          :project-id="projectId">
        </DocumentExporter>

        <b-modal v-model="showDeleteConfirmModal"
                 ok-variant="danger"
                 ok-title="Delete"
                 :ok-disabled="deleteLocked"
                 @ok="deleteDocumentsAndAnnotationHandler"
                 @hidden="deleteLocked = true"
                 :title="'Delete ' + selectedDocuments.length + ' documents and ' + selectedAnnotations.length + ' annotations'">

          <p class="badge badge-danger">Warning, this action is permanent!</p>
          <p class="badge badge-danger">Deleting a document will also delete their associated annotations.</p>

          <p>Are you sure you want to delete {{ selectedDocuments.length }} documents and
            {{ selectedAnnotations.length }} annotations?</p>

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



        <div v-if="documents">
          <b-overlay :show="loading">
            <DocumentsList ref="docsList" :documents="documents"
                           @selection-changed="docAnnoSelectionChanged"></DocumentsList>
          </b-overlay>
        </div>
        <div v-else>
          No documents uploaded
        </div>
      </b-tab>

      <b-tab title="Annotators" :disabled="!local_project.is_configured">
        <h2 class="mt-2 mb-2">Annotators Management
          <b-icon-question-circle id="project-annotators-help" scale="0.5"
                                  style="cursor:pointer;"></b-icon-question-circle>
        </h2>
        <b-popover target="project-annotators-help" triggers="hover" placement="bottom">
          Add annotators to the project by clicking on the list of names in the <strong>right column</strong>. Current
          annotators can be removed
          by clicking on the names in the <strong>left column</strong>. Removing annotators does not delete their
          completed annotations
          but will stop their current pending annotation task.

        </b-popover>
        <Annotators :projectID="projectId"></Annotators>
      </b-tab>

    </b-tabs>


  </div>
</template>

<script>
import _ from "lodash"
import {mapActions, mapState} from "vuex";
import VTable from "@/components/VTable";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import Annotators from "@/components/Annotators";
import JsonEditor from "@/components/JsonEditor";
import VJsoneditor from "v-jsoneditor";
import {readFileAsync, toastError, toastSuccess} from "@/utils";
import DocumentsList from "@/components/DocumentsList";
import MarkdownEditor from "@/components/MarkdownEditor";
import ProjectIcon from "@/components/ProjectIcon";
import ProjectStatusBadges from "@/components/ProjectStatusBadges";
import DocumentUploader from "@/components/DocumentUploader";
import DocumentExporter from "@/components/DocumentExporter";

export default {
  name: "Project",
  title() {
    return `Project - ${this.local_project.name}`
  },
  components: {
    DocumentExporter,
    DocumentUploader,
    ProjectStatusBadges,
    ProjectIcon,
    MarkdownEditor, DocumentsList, JsonEditor, AnnotationRenderer, VTable, VJsoneditor, Annotators},
  data() {
    return {
      activeTab: 0,
      annotationOutput: {},
      local_project: {
        name: null,
        description: "",
        annotator_guideline: "",
        configuration: null,
        data: null,
        annotations_per_doc: 3,
        annotator_max_annotation: 0.6,
        allow_document_reject: true,
        document_input_preview: {},
        is_configured: false,
        is_completed: false,
        document_id_field: "",
      },
      configurationStr: "",
      documents: [],
      selectedDocuments: [],
      selectedAnnotations: [],
      showDeleteConfirmModal: false,
      showDocumentUploadModal: false,
      showDocumentExportModal: false,
      deleteLocked: true,
      loading: false,
    }
  },
  props: {
    projectId: {
      type: String,
    }

  },
  computed: {
    ...mapState(["projects"]),
    projectConfigValid() {
      return this.local_project && this.local_project.configuration && this.local_project.configuration.length > 0
    },
    projectReadyForAnnotation() {
      return this.projectConfigValid()
    },
    loadingVariant() {
      if (this.loading) {
        return "secondary"
      } else {
        return "primary"
      }
    },
    loadingIconAnimation() {
      if (this.loading) {
        return "throb"
      }

      return null
    },
    numDocs() {
      return this.documents.length
    },
    numAnnotations() {
      let numAnnotations = 0
      for (let doc of this.documents) {
        numAnnotations += doc.annotations.length
      }

      return numAnnotations
    }

  },
  methods: {
    ...mapActions(["getProject",
      "updateProject", "getProjectDocuments", "getAnnotations", "addProjectDocument",
      "deleteDocumentsAndAnnotations", "importProjectConfiguration", "exportProjectConfiguration", "cloneProject"]),
    async fetchProject() {
      try {
        if (this.projectId) {
          this.local_project = await this.getProject(this.projectId)
          this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError(this, "Could not fetch project information from server")
      }

    },
    async refreshDocumentsHandler() {
      this.setLoading(true)
      try {
        this.documents = await this.getProjectDocuments(this.projectId)
      } catch (e) {
        toastError(this, "Could not reload document", e)
      }
      this.setLoading(false)
    },
    async saveProjectHandler() {
      this.setLoading(true)
      try {
        await this.updateProject(this.local_project);
        await this.fetchProject()
        toastSuccess(this, "Save project configuration", "Save successful")
      } catch (e) {
        toastError(this, "Could not save project configuration", e)
      }
      this.setLoading(false)
    },
    async importProjectConfigHandler(e) {
      this.setLoading(true)
      try {
        const fileList = e.target.files
        try {
          let file = fileList[0]
          const configStr = await readFileAsync(file)
          const config = JSON.parse(configStr)
          await this.importProjectConfiguration({id: this.projectId, config_dict: config})
          await this.fetchProject()
          toastSuccess(this, "Project configuration imported")

        } catch (e) {
          console.error("Could not parse uploaded file")
          console.error(e)
          toastError(this, "Could not parse uploaded file " + file, e)
        }

      } catch (e) {
        toastError(this, "Could not upload configuration file", e)
      }

      this.setLoading(false)

    },
    async exportProjectConfigHandler() {
      try {
        let response = await this.exportProjectConfiguration(this.projectId)
        let fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(response)]));
        let fileLink = document.createElement('a');


        fileLink.href = fileURL;
        fileLink.setAttribute('download', `project${this.projectId}-${this.local_project.name}.json`);
        document.body.appendChild(fileLink);

        fileLink.click();

      } catch (e) {
        toastError(this, "Could export project configuration", e)
      }


    },
    async cloneProjectConfigHandler() {
      try {
        let clonedProjObj = await this.cloneProject(this.projectId)
        this.$router.push("/project/" + clonedProjObj.id)

      } catch (e) {
        toastError(this, "Could export project configuration", e)
      }

    },
    async documentStartUploadHandler(e) {
      this.setLoading(true)
    },
    async documentUploadHandler(e) {
      await this.fetchProject()
      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },

    goToAnnotatePage(e) {
      this.$router.push(`/annotate/${this.projectId}/${this.documents[0].id}`)

    },
    annotationOutputHandler(value) {
      this.annotationOutput = value
    },
    docAnnoSelectionChanged(value) {
      this.selectedDocuments = value.documents
      this.selectedAnnotations = value.annotations
    },
    isEverythingSelected() {
      return this.selectedDocuments.length >= this.numDocs &&
          this.selectedAnnotations.length >= this.numAnnotations
    },
    async deleteDocumentsAndAnnotationHandler(e) {
      try {
        await this.deleteDocumentsAndAnnotations({
          documentIds: this.selectedDocuments,
          annotationIds: this.selectedAnnotations
        })
        toastSuccess(this, "Documents and annotations deleted", this.selectedDocuments.length + "documents and " + this.selectedAnnotations.length + "deleted.")

        await this.refreshDocumentsHandler()

      } catch (e) {
        toastError(this, "Could not delete documents or annotations", e)

      }

    },

  },
  watch: {
    projectId: {
      immediate: true,
      handler() {
        this.fetchProject()
      }
    },
  },
  async beforeMount() {
    this.fetchProject()


  },
}
</script>

<style scoped>

.infoCard {
  background: #838383;
  color: white;
  margin: 1em 0;

}


</style>
