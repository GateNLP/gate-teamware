<template>
  <div>
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
          <b-icon-box-arrow-in-down ></b-icon-box-arrow-in-down>
          Save
        </b-button>
        <b-button @click="$refs.projectConfigImportInput.click()" :variant="loadingVariant" :disabled="loading"
                  title="Import JSON project configuration file.">
          <b-icon-cloud-upload ></b-icon-cloud-upload>
          Import
        </b-button>
        <b-button @click="exportProjectConfigHandler" :variant="loadingVariant" :disabled="loading"
                  title="Export project configuration as a JSON file.">
          <b-icon-cloud-download ></b-icon-cloud-download>
          Export
        </b-button>
        <b-button @click="cloneProjectConfigHandler" :variant="loadingVariant" :disabled="loading"
                  title="Create a new project using this project's configuration. Does not copy documents, annotations or annotator list.">
          <b-icon-clipboard ></b-icon-clipboard>
          Clone project
        </b-button>
        <b-button @click="showDeleteProjectModal=true" variant="danger" :disabled="loading"
                  title="Delete project.">
          <b-icon-x></b-icon-x>
          Delete project
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
        <b-form-input v-model="local_project.document_id_field" name="project_document_id_field"></b-form-input>
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


    <b-modal v-model="showDeleteProjectModal"
             ok-variant="danger"
             ok-title="Delete"
             :ok-disabled="deleteProjectLocked"
             @ok="deleteProjectHandler"
             @hidden="deleteProjectLocked = true"
             :title="'Delete project #' + project.id + ' ' + project.name +  '?'">

      <p class="badge badge-danger">Warning, this action is permanent!</p>
      <p class="badge badge-danger">Deleting the project will also delete all associated documents and annotations.</p>

      <div>
        <b-button @click="deleteProjectLocked = !deleteProjectLocked"
                  :class="{'btn-danger': deleteProjectLocked, 'btn-success': !deleteProjectLocked}"
        >
          <b-icon-lock-fill v-if="deleteProjectLocked"></b-icon-lock-fill>
          <b-icon-unlock-fill v-else></b-icon-unlock-fill>
          <span v-if="deleteProjectLocked">Unlock delete</span>
          <span v-else>Lock delete</span>
        </b-button>

      </div>
    </b-modal>
  </div>

</template>

<script>
import {mapActions, mapState} from "vuex";
import ProjectStatusBadges from "@/components/ProjectStatusBadges";
import ProjectIcon from "@/components/ProjectIcon";
import MarkdownEditor from "@/components/MarkdownEditor";
import JsonEditor from "@/components/JsonEditor";
import AnnotationRenderer from "@/components/AnnotationRenderer";
import VJsoneditor from "v-jsoneditor";
import {readFileAsync, toastError, toastSuccess} from "@/utils";


export default {
  name: "ProjectConfiguration",
  components: {
    ProjectStatusBadges,
    ProjectIcon,
    MarkdownEditor, JsonEditor, AnnotationRenderer, VJsoneditor},
  data() {
    return {
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
      annotationOutput: {},
      configurationStr: "",
      showDeleteProjectModal: false,
      deleteProjectLocked: true,
      loading: false,
    }
  },
  props: {
    project: {
      default: null,
    }
  },
  watch: {
    project: {
      immediate: true,
      handler(newValue){
        this.local_project = newValue
      }
    }
  },
  computed: {
    loadingVariant() {
      if (this.loading) {
        return "secondary"
      } else {
        return "primary"
      }
    },
  },
  methods: {
    ...mapActions(["getProject", "deleteProject",
      "updateProject", "importProjectConfiguration", "exportProjectConfiguration", "cloneProject"]),
    async saveProjectHandler() {
      this.setLoading(true)
      try {
        await this.updateProject(this.local_project);
        this.$emit("updated")
        console.log("Updated")
        toastSuccess("Save project configuration", "Save successful", this)
      } catch (e) {
        console.log("Not updated")
        toastError("Could not save project configuration", e, this)
      }
      this.setLoading(false)
    },
    async deleteProjectHandler(){
      try{
        await this.deleteProject(this.local_project.id)
        toastSuccess("Project deleted", "The project has been deleted", null)
        this.$router.push("/projects")
      }catch(e){
        toastError("Could not delete project", e, null)
      }
    },
    async importProjectConfigHandler(e) {
      this.setLoading(true)
      try {
        const fileList = e.target.files
        try {
          let file = fileList[0]
          const configStr = await readFileAsync(file)
          const config = JSON.parse(configStr)
          await this.importProjectConfiguration({id: this.local_project.id, config_dict: config})
          this.$emit("updated")
          toastSuccess("Project configuration imported", undefined, this)

        } catch (e) {
          console.error("Could not parse uploaded file")
          console.error(e)
          toastError("Could not parse uploaded file " + file, e, this)
        }

      } catch (e) {
        toastError("Could not upload configuration file", e, this)
      }

      this.setLoading(false)

    },
    async exportProjectConfigHandler() {
      try {
        let response = await this.exportProjectConfiguration(this.local_project.id)
        let fileURL = window.URL.createObjectURL(new Blob([JSON.stringify(response)]));
        let fileLink = document.createElement('a');


        fileLink.href = fileURL;
        fileLink.setAttribute('download', `project${this.local_project.id}-${this.local_project.name}.json`);
        document.body.appendChild(fileLink);

        fileLink.click();

      } catch (e) {
        toastError("Could export project configuration", e, this)
      }


    },
    async cloneProjectConfigHandler() {
      try {
        let clonedProjObj = await this.cloneProject(this.local_project.id)
        this.$router.push("/project/" + clonedProjObj.id)

      } catch (e) {
        toastError("Could export project configuration", e, this)
      }

    },
    annotationOutputHandler(value) {
      this.annotationOutput = value
    },
    async setLoading(isLoading) {
      this.loading = isLoading
    },
  }

}
</script>

<style scoped>

</style>
