<template>
  <div class="container">
    <h1>Project: {{ local_project.name }}</h1>

    <b-tabs v-model="activeTab">
      <b-tab title="Configuration">

        <h2 class="mt-2 mb-2">Project configuration</h2>
        <b-button-toolbar class="mt-2 mb-2">
          <b-button-group>
            <b-button @click="saveProjectHandler" :variant="loadingVariant" :disabled="loading">
            <b-icon-box-arrow-in-down :animation="loadingIconAnimation"></b-icon-box-arrow-in-down>
            Save config
          </b-button>
          <b-button @click="$refs.projectConfigImportInput.click()" :variant="loadingVariant" :disabled="loading">
            <b-icon-cloud-upload :animation="loadingIconAnimation"></b-icon-cloud-upload>
            Import config
          </b-button>
          <b-button @click="exportProjectConfigHandler" :variant="loadingVariant" :disabled="loading">
            <b-icon-cloud-download :animation="loadingIconAnimation"></b-icon-cloud-download>
            Export config
          </b-button>

          </b-button-group>
        </b-button-toolbar>

        <input ref="projectConfigImportInput" type="file" accept=".json" @change="importProjectConfigHandler" hidden/>

        <b-card class="infoCard">
          The project can be configured on this page with name, description and how annotations are captured.
          Once you've configured the project, don't forget to <strong>save project configuration</strong> using the
          button above.
          Documents &amp; annotations can be added and managed on the <a href="#" @click.prevent="activeTab = 1">Documents
          &amp; Annotations</a> page.
          Annotators can be recruited by using the <a href="#" @click.prevent="activeTab = 2">Annotators</a> page.

        </b-card>

        <b-form class="mt-4 mb-4">
          <b-form-group label="Name" description="The name of this annotation project.">
            <b-form-input v-model="local_project.name" name="project_name"></b-form-input>
          </b-form-group>
          <b-form-group label="Description" description="The description of this annotation project that will be shown to annotators. Supports markdown and HTML.">
            <MarkdownEditor v-model="local_project.description"></MarkdownEditor>
          </b-form-group>
          <b-form-group label="Annotator guideline" description="The description of this annotation project that will be shown to annotators. Supports markdown and HTML.">
            <MarkdownEditor v-model="local_project.annotator_guideline"></MarkdownEditor>
          </b-form-group>
          <b-form-group label="Annotations per document" description="The project completes when each document in this annotation project have this many number of valid annotations. When a project completes, all project annotators will be un-recruited and be allowed to annotate other projects.">
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
          <b-form-row>
            <b-col>
              <h4 id="annotation-preview">Annotation configuration</h4>
              <p class="form-text text-muted">Configure how the project will capture annotations below. The configuration
              is in JSON format, you must provide a list of widgets to use for displaying information or capturing annotations.
                See the <a target="_blank" href="https://gatenlp.github.io/gate-annotation-service/userguide/projectconfig.html">documentation page on configuring project annotation</a>
                for more details.</p>
              <JsonEditor v-model="local_project.configuration"></JsonEditor>
            </b-col>
            <b-col>
              <h4>Annotation preview</h4>
              <p class="form-text text-muted">A live preview of what annotators will see according to the annotation
                configuration. You can use this to test the
                behaviour of the annotation widgets. Press <strong>Submit</strong> to check validation behaviour. Output
                of the annotation
                is shown in the <a href="#annotation-output-preview">Annotation output preview</a> below.</p>
              <b-card>
                <AnnotationRenderer  :config="local_project.configuration" :document="local_project.document_input_preview"
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
              <VJsoneditor v-model="local_project.document_input_preview" :options="{mode: 'code'}" :plus="false" height="400px"></VJsoneditor>
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
        <h2 class="mt-2 mb-2">Documents & Annotations</h2>

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
            <b-button variant="primary" @click="$refs.documentUploadInput.click()" title="Upload documents">
              <b-icon-upload></b-icon-upload>
              Upload
            </b-button>
            <b-button variant="primary" @click="exportAnnotationsHandler" title="Export documents with annotation.">
              <b-icon-download></b-icon-download>
              Export
            </b-button>

          </b-button-group>

          <input ref="documentUploadInput" type="file" @change="documentUploadHandler" multiple hidden/>


        </b-button-toolbar>

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

        <b-card class="infoCard">
          You can view the list of documents and annotations of this project on this page.
          Start by <a href="#" @click.prevent="uploadBtnHandler">uploading</a> documents to the project,
          documents must be in a JSON format. Annotators can then be recruited by using the <a href="#"
                                                                                               @click.prevent="activeTab = 2">Annotators</a>
          page.
        </b-card>

        <b-card>
          <h4>Project documents & annotations summary</h4>
          <p class="form-text text-muted">
            Current annotation status of the project.
          </p>
          <div>
            <b-badge variant="success" class="mr-2" title="Completed annotations">
              <b-icon-pencil-fill></b-icon-pencil-fill>
              {{ local_project.completed_tasks }}
            </b-badge>
            <b-badge variant="danger" class="mr-2" title="Rejected annotations">
              <b-icon-x-square-fill></b-icon-x-square-fill>
              {{ local_project.rejected_tasks }}
            </b-badge>
            <b-badge variant="warning" class="mr-2" title="Timed out annotations">
              <b-icon-clock></b-icon-clock>
              {{ local_project.timed_out_tasks }}
            </b-badge>
            <b-badge variant="secondary" class="mr-2" title="Aborted annotations">
              <b-icon-stop-fill></b-icon-stop-fill>
              {{ local_project.aborted_tasks }}
            </b-badge>
            <b-badge variant="primary" class="mr-2" title="Pending annotations">
              <b-icon-play-fill></b-icon-play-fill>
              {{ local_project.pending_tasks }}
            </b-badge>
            <b-badge variant="dark" class="mr-2" title="Occupied (completed & pending)/Total tasks">
              <b-icon-card-checklist></b-icon-card-checklist>
              {{ local_project.completed_tasks + local_project.pending_tasks }}/{{ local_project.total_tasks }}
            </b-badge>
            <b-badge variant="info" class="mr-2" title="Number of documents">
              <b-icon-file-earmark-fill></b-icon-file-earmark-fill>
              {{ local_project.documents }}
            </b-badge>

          </div>
        </b-card>


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

      <b-tab title="Annotators">
        <h2 class="mt-2 mb-2">Annotators Management</h2>
        <b-card class="infoCard">
          Add annotators to the project by clicking on the list of names in the <strong>right column</strong>. Current
          annotators can be removed
          by clicking on the names in the <strong>left column</strong>. Removing annotators does not delete their
          completed annotations
          but will stop their current pending annotation task.
        </b-card>
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

export default {
  name: "Project",
  title() {
    return `Project - ${this.local_project.name}`
  },
  components: {MarkdownEditor, DocumentsList, JsonEditor, AnnotationRenderer, VTable, VJsoneditor, Annotators},
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
        document_input_preview: {}
      },
      configurationStr: "",
      documents: [],
      selectedDocuments: [],
      selectedAnnotations: [],
      showDeleteConfirmModal: false,
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
    ...mapActions(["getProjects",
      "updateProject", "getProjectDocuments", "getAnnotations", "addProjectDocument",
      "deleteDocumentsAndAnnotations", "importProjectConfiguration", "exportProjectConfiguration"]),
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
        this.documents = await this.getProjectDocuments(this.projectId)
        toastSuccess(this, "Save project configuration", "Save successful")
      } catch (e) {
        toastError(this, "Could not save project configuration", e)
      }
      this.setLoading(false)
    },
    async importProjectConfigHandler(e){
      this.setLoading(true)
      try {
        const fileList = e.target.files

        for (let file of fileList) {
          try {
            const configStr = await readFileAsync(file)
            const config = JSON.parse(configStr)
            await this.importProjectConfiguration({id: this.projectId, config_dict: config})
            await this.getProjects()
            toastSuccess(this,"Project configuration imported")

          } catch (e) {
            console.error("Could not parse uploaded file")
            console.error(e)
            toastError(this, "Could not parse uploaded file " + file, e)
          }

          this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError(this, "Could not upload configuration file", e)
      }

      this.setLoading(false)

    },
    async exportProjectConfigHandler(){
      try{
        let response = await this.exportProjectConfiguration(this.projectId)
        let fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(response)]));
        let fileLink = document.createElement('a');


        fileLink.href = fileURL;
        fileLink.setAttribute('download', `project${this.projectId}-${this.local_project.name}.json`);
        document.body.appendChild(fileLink);

        fileLink.click();

      }catch (e){
        toastError(this, "Could export project configuration", e)
      }


    },
    async documentUploadHandler(e) {

      this.setLoading(true)
      try {
        const fileList = e.target.files

        for (let file of fileList) {
          try {
            const documentsStr = await readFileAsync(file)
            const documents = JSON.parse(documentsStr)
            // Uploaded file must be an array of docs
            if (documents instanceof Array) {
              for (let document of documents) {
                await this.addProjectDocument({projectId: this.projectId, document: document})
              }
            }

          } catch (e) {
            console.error("Could not parse uploaded file")
            console.error(e)
            toastError(this, "Could not parse uploaded file " + file, e)
          }

          this.documents = await this.getProjectDocuments(this.projectId);
        }

      } catch (e) {
        toastError(this, "Could not upload document", e)
      }

      this.setLoading(false)
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
    async exportAnnotationsHandler() {
      try{
        let response = await this.getAnnotations(this.projectId)
        let fileURL = window.URL.createObjectURL(new Blob([response]));
        let fileLink = document.createElement('a');


        fileLink.href = fileURL;
        fileLink.setAttribute('download', 'annotations.json');
        document.body.appendChild(fileLink);

        fileLink.click();

      }catch (e){
        toastError(this, "Could not export annotations", e)
      }


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
    projects: {
      immediate: true,
      handler(newProjectsList) {
        if (this.projectId && newProjectsList) {
          for (let project of newProjectsList) {
            if (String(project.id) === this.projectId) {
              this.local_project = _.cloneDeep(project)

            }
          }
        }
      }
    },
  },
  async beforeMount() {
    await this.getProjects();
    this.documents = await this.getProjectDocuments(this.projectId);

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
