<template>
  <div>
    <b-tabs>
      <b-tab title="Code">

      <slot></slot>

      </b-tab>
      <b-tab title="Preview">
        <b-card class="mb-2 mt-2">
          <AnnotationRenderer :config="config"
                              :document="document" :allow_document_reject="true"
                              v-model="annotationOutput"
                              :doc_preannotation_field="preAnnotation"
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
      annotationOutput: {}

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
  }
}
</script>

<style>
legend {
font-weight: bold;
}
</style>
