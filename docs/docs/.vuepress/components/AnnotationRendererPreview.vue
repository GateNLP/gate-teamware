<template>
  <div>
    <b-tabs>
      <b-tab title="Code">

      <slot></slot>

      </b-tab>
      <b-tab title="Preview">
        <p v-if="documents.length > 1">Document {{documentIndex + 1}} of {{documents.length}}</p>
        <b-card class="mb-2 mt-2">
          <AnnotationRenderer ref="annotationRenderer"
                              :config="config"
                              :document="currentDocument" :allow_document_reject="true"
                              v-model="annotationOutput"
                              :doc_preannotation_field="preAnnotation"
                              @submit="nextDocument()"
                              @reject="nextDocument()"
          ></AnnotationRenderer>
        </b-card>
        <b-card class="mb-2 mt-2">
          <p><strong>Annotation output:</strong></p>
          {{annotationOutput}}
        </b-card>
      </b-tab>

    </b-tabs>
  </div>

</template>

<script>
import AnnotationRenderer from '@/components/AnnotationRenderer';

export default {
  name: "AnnotationRendererPreview",
  components: {
    AnnotationRenderer
  },
  data(){
    return {
      annotationOutput: {},
      documentIndex: 0
    }

  },
  computed: {
    documents() {
      if(Array.isArray(this.document)) {
        return this.document
      } else {
        return [this.document]
      }
    },
    currentDocument() {
      return this.documents[this.documentIndex]
    }
  },
  props: {
    preAnnotation: {
      default(){
        return ""
      }
    },
    document: {
      default(){
        return {text: "Sometext with <strong>html</strong>"}
      }
    },
    config: {
      default() {
        return [
            {
              "name": "htmldisplay",
              "type": "html",
              "text": "{{{text}}}"
            },
            {
              "name": "sentiment",
              "type": "radio",
              "title": "Sentiment",
              "description": "Please select a sentiment of the text above.",
              "options": {
                "negative": "Negative",
                "neutral": "Neutral",
                "positive": "Positive"

              }
            }
          ]
      }
    },
  },
  methods: {
    nextDocument() {
      this.documentIndex = (this.documentIndex + 1) % this.documents.length;
      this.$refs.annotationRenderer.clearForm()
    }
  }
}
</script>

<style>
legend {
font-weight: bold;
}
</style>
