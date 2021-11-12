---
sidebarDepth: 3
---

# Project configuration

The **Configuration** tab in the **Project management** page allows you to change project settings including what
annotations are captured.

Project configurations can be imported and exported in the format of a JSON file.

The project can be also be cloned (have configurations copied to a new project). Note that cloning does not copy
documents, annotations or annotators to the new project.

## Configuration fields

* **Name** - The name of this annotation project.
* **Description** - The description of this annotation project that will be shown to annotators. Supports markdown and
  HTML.
* **Annotator guideline** - The description of this annotation project that will be shown to annotators. Supports
  markdown and HTML.
* **Annotations per document** - The project completes when each document in this annotation project have this many
  number of valid annotations. When a project completes, all project annotators will be un-recruited and be allowed to
  annotate other projects.
* **Maximum proportion of documents annotated per annotator (between 0 and 1)** - A single annotator cannot annotate
  more than this proportion of documents.
* **Timeout for pending annotation tasks (minutes)** - Specify the number of minutes a user has to complete an
  annotation task (i.e. annotating a single document).
* **Document ID field** - The field in your uploaded documents that is used as a unique identifier. GATE's json format
  uses the name field. You can use a dot limited key path to access subfields e.g. enter features.name to get the id
  from the object `{'features':{'name':'nameValue'}}`

## Anotation configuration

The annotation configuration takes a `json` string for configuring how the document is displayed to the user and types
of annotation will be collected. Here's an example configuration and a preview of how it is shown to annotators:


<AnnotationRendererPreview :config="configs.config1">

```json
// Example configuration
[
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
```

</AnnotationRendererPreview>

Within the configuration, it is possible to specify how your documents will be displayed. The **Document input preview** 
box can be used to provide a sample of your document for rendering of the preview. 

```json
// Example contents for the Document input preview
{
  "text": "Sometext with <strong>html</strong>"
}
```



The above configuration displays the value from the `text` field from the document to be annotated. It then shows a set
of 3 radio inputs that allows the user to select a Negative, Neutral, or Positive sentiment with the label
name `sentiment`.



All fields **require** the properties **name** and **type**, it is used to name our label and determine the type of
input/display to be shown to the user respectively.

Another field can be added to collect more information, e.g. a text field for opinions:

<AnnotationRendererPreview :config="configs.config2">

```json
[
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
    },
    {
        "name": "opinion",
        "type": "text",
        "title": "What's your opinion of the above text?",
        "optional": true
    }

]
```

</AnnotationRendererPreview>

Note that for the above case, the `optional` field is added ensure that allows user to not have to input any value.
This `optional` field can be used on all components.

Some fields are available to configure which are specific to components, e.g. the `options` field are only available for
the `radio`, `checkbox` and `selector` components. See details below on the usage of each specific component.

The captured annotation results in a JSON dictionary, an example can be seen in the **Annotation output preview** box.
The annotation is linked to a Document and is converted to a GATE JSON annotation format when exported.

### Displaying text

<AnnotationRendererPreview :config="configs.configDisplay">

```json
[
    {
        "name": "htmldisplay",
        "type": "html",
        "text": "{{{text}}}"
    }
]
```

</AnnotationRendererPreview>

### Text input

<AnnotationRendererPreview :config="configs.configTextInput">

```json
[
    {
        "name": "mylabel",
        "type": "text",
        "optional": true, //Optional - Set if validation is not required
        "regex": "regex string", //Optional - When specified, the regex pattern will used to validate the text
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message then field is validated", //Optional
        "valError": "Error message when field fails is validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Textarea input

<AnnotationRendererPreview :config="configs.configTextarea">

```json
[
    {
        "name": "mylabel",
        "type": "textarea",
        "optional": true, //Optional - Set if validation is not required
        "regex": "regex string", //Optional - When specified, the regex pattern will used to validate the text
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message then field is validated", //Optional
        "valError": "Error message when field fails is validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Radio input

<AnnotationRendererPreview :config="configs.configRadio">

```json
[
    {
        "name": "mylabel",
        "type": "radio",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1",
            "value2": "Text to show user 2",
            "value3": "Text to show user 3",
        },
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message then field is validated", //Optional
        "valError": "Error message when field fails is validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Checkbox input

<AnnotationRendererPreview :config="configs.configCheckbox">

```json
[
    {
        "name": "mylabel",
        "type": "checkbox",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1",
            "value2": "Text to show user 2",
            "value3": "Text to show user 3",
        },
        "minSelected": 1, //Optional - Overrides optional field. Specify the minimum number of options that must be selected
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message then field is validated", //Optional
        "valError": "Error message when field fails is validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Selector input

<AnnotationRendererPreview :config="configs.configSelector">

```json
[
    {
        "name": "mylabel",
        "type": "selector",
        "optional": true, //Optional - Set if validation is not required
        "options": { // The options that the user is able to select from
            "value1": "Text to show user 1",
            "value2": "Text to show user 2",
            "value3": "Text to show user 3",
        },
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message then field is validated", //Optional
        "valError": "Error message when field fails is validation" //Optional
    }
]
```

</AnnotationRendererPreview>


<script>
import configs from './config_examples';
export default {
  computed: {
    configs(){ return configs }
  }

}
</script>
