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
* **Reject documents** - Switching this off will mean that annotators for this project will be unable to choose to reject documents.
* **Document ID field** - The field in your uploaded documents that is used as a unique identifier. GATE's json format
  uses the name field. You can use a dot limited key path to access subfields e.g. enter features.name to get the id
  from the object `{'features':{'name':'nameValue'}}`
* **Training stage enable/disable** - Enable or disable training stage, allows testing documents to be uploaded to the project. 
* **Test stage enable/disable** - Enable or disable testing stage, allows test documents to be uploaded to the project.
* **Auto elevate to annotator** - The option works in combination with the training and test stage options, see table below for the behaviour:

  | Training stage | Testing stage | Auto elevate to annotator | Desciption |
  | --- | --- | --- | --- |
  | Disabled | Disabled | Enabled/Disabled | User allowed to annotate without manual approval. |
  | Enabled | Disabled | Disabled | Manual approval required. |
  | Disabled | Enabled | Disabled | " |
  | Enabled | Disabled | Enabled | User always allowed to annotate after training phase completed |
  | Disabled | Enabled | Enabled | User automatically allowed to annotate after passing test, if user fails test they have to be manually approved. |
  | Enabled | Enabled | Enabled | " |

* **Test pass proportion** - The proportion of correct test annotations to be automatically allowed to annotate documents.
* **Gold standard field** - The field in document's JSON/column that contains the ideal annotation values and explanation for the annotation.
* **Pre-annotation** - Pre-fill the form with annotation provided in the specified field. See [Importing Documents with pre-annotation](./documents_annotations_management.md#importing-documents-with-pre-annotation) section for more detail.

## Annotation configuration

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
    "options": [
      {"value": "negative", "label": "Negative"},
      {"value": "neutral", "label": "Neutral"},
      {"value": "positive", "label": "Positive"}
    ]
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
        "options": [
            {"value": "negative", "label": "Negative"},
            {"value": "neutral", "label": "Neutral"},
            {"value": "positive", "label": "Positive"}
        ]
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
This `optional` field can be used on all components.  Any component may optionally have a field named `if`, containing an expression that is used to determine whether or not the component appears based on information in the document and/or the values entered in the other components.  For example the user could be presented with a set of options that includes an "other" choice, and if the annotator chooses "other" then an additional free text field appears for them to fill in.  The `if` option is described in more detail under the [conditional components](#conditional-components) section below.

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
        "text": "{{{text}}}" // The text that will be displayed
    }
]
```

</AnnotationRendererPreview>

The `htmldisplay` widget allows you to display the text you want annotated. It accepts almost full range of HTML
input which gives full styling flexibility. 

Any field/column from the document can be inserted by surrounding a field/column name with double or 
triple curly brackets. Double curly brackets renders text as-is and triple curly brackets accepts HTML string:

<AnnotationRendererPreview :config="configs.configDisplayHtmlNoHtml">

Input:

```json
{
  "text": "Sometext with <strong>html</strong>"
}
```

Configuration, showing the same field/column in document as-is or as HTML:
```json
[
    {
        "name": "htmldisplay",
        "type": "html",
        "text": "No HTML: {{text}} <br/> HTML: {{{text}}}"
    }
]
```

</AnnotationRendererPreview>

The widget makes no assumption about your document structure and any field/column names can be used, 
even sub-fields by using the dot notation e.g. `parentField.childField`:

<AnnotationRendererPreview :config="configs.configDisplayCustomFieldnames" :document="configs.doc2">

JSON input:

```json
{
    "customField": "Content of custom field.",
    "anotherCustomField": "Content of another custom field.",
    "subfield": {
        "subfieldContent": "Content of a subfield."
    }
}
```

or in csv

| customField | anotherCustomField | subfield.subfieldContent |
| --- | --- | --- |
| Content of custom field. | Content of another custom field. | Content of a subfield. |


Configuration, showing the same field/column in document as-is or as HTML:
```json
[
    {
        "name": "htmldisplay",
        "type": "html",
        "text": "Custom field: {{customField}} <br/> Another custom field: {{{anotherCustomField}}} <br/> Subfield: {{{subfield.subfieldContent}}}"
    }
]
```

</AnnotationRendererPreview>

If your documents are plain text and include line breaks that need to be preserved when rendering, this can be achieved by using a special HTML wrapper which sets the [`white-space` CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space).

<AnnotationRendererPreview :config="configs.configDisplayPreserveNewlines" :document="configs.docPlainText">

**Document**

```json
{
    "text": "This is some text\n\nIt has line breaks that we want to preserve."
}
```

**Project configuration**

```json
[
    {
        "name": "htmldisplay",
        "type": "html",
        "text": "<div style='white-space: pre-line'>{{text}}</div>"
    }
]
```

</AnnotationRendererPreview>

`white-space: pre-line` preserves line breaks but collapses other whitespace down to a single space, `white-space: pre-wrap` would preserve all whitespace including indentation at the start of a line, but would still wrap lines that are too long for the available space.

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
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
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
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
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
        "orientation": "vertical", //Optional - default is "horizontal"
        "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
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
        "orientation": "horizontal", //Optional - "horizontal" (default) or "vertical"
        "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
        "minSelected": 1, //Optional - Overrides optional field. Specify the minimum number of options that must be selected
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Richer labels for radios & checkboxes

The `label` of radio and checkbox inputs is normally plain text, however both input types support an `htmlLabel` property as an alternative to `label`, which allows for HTML tags within the option label.  The `htmlLabel` is rendered within a `<span></span>` inside the `<label>` element for the option, so it should be limited to presentational tags such as `<em>`, `<b>`, `<tt>`, or custom CSS directives via `<span style='...'>` or `<div style='...'>`.  In particular a `<div style='margin-bottom: 1.5em'>` is a convenient way to break up a long list of radio buttons (with `"orientation": "vertical"`) into logical sections.

<AnnotationRendererPreview :config="configs.configHtmlLabels">

```json
[
  {
    "name": "sentiment",
    "type": "checkbox",
    "title": "Sentiment",
    "options": [
      {
        "value": "positive",
        "htmlLabel": "<span style='color: green'>Positive</span>"
      },
      {
        "value": "neutral",
        "htmlLabel": "<span style='font-style: italic'>Neutral</span> or uncertain"
      },
      {
        "value": "positive",
        "htmlLabel": "<span style='color: red'>Negative</span>"
      }
    ]
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
        "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1"},
                {"value": "value2", "label": "Text to show user 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Optional help text

Optionally, radio buttons and checkboxes can be given help text to provide additional per-choice context or information to help annotators.


<AnnotationRendererPreview :config="configs.configRadioHelpText">

```json
[
    {
        "name": "mylabel",
        "type": "radio",
        "optional": true, //Optional - Set if validation is not required
        "orientation": "vertical", //Optional - default is "horizontal"
        "options": [ // The options that the user is able to select from
                {"value": "value1", "label": "Text to show user 1", "helptext": "Additional help text for option 1"},
                {"value": "value2", "label": "Text to show user 2", "helptext": "Additional help text for option 2"},
                {"value": "value3", "label": "Text to show user 3"}
            ],
        "title": "Title string", //Optional
        "description": "Description string", //Optional
        "valSuccess": "Success message when the field is validated", //Optional
        "valError": "Error message when the field fails validation" //Optional
    }
]
```

</AnnotationRendererPreview>

### Alternative way to provide options for radio, checkbox and selector<a id='options-as-dict'></a>

A dictionary (key value pairs) and also be provided to the `options` field of the radio, checkbox and selector widgets
but note that the ordering of the options are **not guaranteed** as javascript does not sort dictionaries by
the order in which keys are added. Note that additional help texts for radio buttons and checkboxes are not supported using this syntax.

<AnnotationRendererPreview :config="configs.configRadioDict">

```json
[
    {
          "name": "mylabel",
          "type": "radio",
          "optional": true, //Optional - Set if validation is not required
          "options": { // The options can be specified as a dictionary, ordering is not guaranteed
              "value1": "Text to show user 1",
              "value2": "Text to show user 2",
              "value3": "Text to show user 3"
          },
          "title": "Title string", //Optional
          "description": "Description string", //Optional
          "valSuccess": "Success message when the field is validated", //Optional
          "valError": "Error message when the field fails validation" //Optional
      }
]
```

</AnnotationRendererPreview>

### Dynamic options for radio, checkbox and selector

All the examples above have a "static" list of available options for the radio, checkbox and selector widgets, where the complete options list is enumerated in the project configuration and every document offers the same set of options.  However it is also possible to take some or all of the options from the _document_ data rather than the _configuration_ data.  For example:

<AnnotationRendererPreview :config="configs.configDbpediaExample" :document="configs.docDbpediaExample">

**Project configuration**

```json
[
  {
    "name": "uri",
    "type": "radio",
    "title": "Select the most appropriate URI",
    "options":[
      {"fromDocument": "candidates"},
      {"value": "none", "label": "None of the above"},
      {"value": "unknown", "label": "Cannot be determined without more context"}
    ]
  }
]
```

**Document**

```json
{
  "text": "President Bush visited the air base yesterday...",
  "candidates": [
    {
      "value": "http://dbpedia.org/resource/George_W._Bush",
      "label": "George W. Bush (Jnr)"
    },
    {
      "value": "http://dbpedia.org/resource/George_H._W._Bush",
      "label": "George H. W. Bush (Snr)"
    }
  ]
}
```

</AnnotationRendererPreview>

`"fromDocument"` is a dot-separated property path leading to the location within each document where the additional options can be found, for example `"fromDocument":"candidates"` looks for a top-level property named `candidates` in each document, `"fromDocument": "options.custom"` would look for a property named `options` which is itself an object with a property named `custom`.  The target property in the document may be in any of the following forms:

- an array _of objects_, each with `value` and `label` (and optionally `helptext`) properties, exactly as in the static configuration format - this is the format used in the example above
- an array _of strings_, where the same string will be used as both the value and the label for that option
- an arbitrary ["dictionary"](#options-as-dict) object mapping values to labels
- a _single string_, which is parsed into a list of options

The "single string" alternative is designed to be easier to use when [importing documents](documents_annotations_management.md#importing-documents) from CSV files.  It allows you to provide any number of options in a _single_ CSV column value.  Within the column the options are separated by semicolons, and each option is of the form `value=label`.  Whitespace around the delimiters is ignored, both between options and between the value and label of a single option.  For example given CSV document data of

| text            | options                                           |
|-----------------|---------------------------------------------------|
| Favourite fruit | `apple=Apples; orange = Oranges; kiwi=Kiwi fruit` |

a `{"fromDocument": "options"}` configuration would produce the equivalent of

```json
[
  {"value": "apple", "label": "Apples"},
  {"value": "orange", "label": "Oranges"},
  {"value": "kiwi", "label": "Kiwi fruit"}
]
```

If your values or labels may need to contain the default separator characters `;` or `=` you can select different separators by adding extra properties to the configuration:

```json
{"fromDocument": "options", "separator": "~~", "valueLabelSeparator": "::"}
```

| text            | options                                              |
|-----------------|------------------------------------------------------|
| Favourite fruit | `apple::Apples ~~ orange::Oranges ~~ kiwi::Kiwi fruit` |

The separators can be more than one character, and you can set `"valueLabelSeparator":""` to disable label splitting altogether and just use the value as its own label.

### Mixing static and dynamic options

Static and `fromDocument` options may be freely interspersed in any order, so you can have a fully-dynamic set of options by specifying _only_ a `fromDocument` entry with no static options, or you can have static options that are listed first followed by dynamic options, or dynamic options first followed by static, etc.

### Conditional components

By default all components listed in the project configuration will be shown for all documents. However this is not always appropriate, for example you may have some components that are only relevant to certain documents, or only relevant for particular combinations of values in _other_ components.  To allow for these kinds of scenarios any component can have a field named `if` specifying the conditions under which that component should be shown.

The `if` field is an _expression_ that is able to refer to fields in both the current _document_ being annotated and the current state of the other annotation components.  The expression language is largely based on a subset of the standard JavaScript expression syntax but with a few additional syntax elements to ease working with array data and regular expressions.

The following simple example shows how you might implement an "Other (please specify)" pattern, where the user can select from a list of choices but also has the option to supply their own answer if none of the choices are appropriate.  The free text field is only shown if the user selects the "other" choice.

<AnnotationRendererPreview :config="configs.configConditional1" :document="configs.docDbpediaExample">

**Project configuration**

```json
[
  {
    "name": "uri",
    "type": "radio",
    "title": "Select the most appropriate URI",
    "options":[
      {"fromDocument": "candidates"},
      {"value": "other", "label": "Other"}
    ]
  },
  {
    "name": "otherValue",
    "type": "text",
    "title": "Please specify another value",
    "if": "annotation.uri == 'other'",
    "regex": "^(https?|urn):",
    "valError": "Please specify a URI (starting http:, https: or urn:)"
  }
]
```

**Document**

```json
{
  "text": "President Bush visited the air base yesterday...",
  "candidates": [
    {
      "value": "http://dbpedia.org/resource/George_W._Bush",
      "label": "George W. Bush (Jnr)"
    },
    {
      "value": "http://dbpedia.org/resource/George_H._W._Bush",
      "label": "George H. W. Bush (Snr)"
    }
  ]
}
```
</AnnotationRendererPreview>

Note that validation rules (such as `optional`, `minSelected` or `regex`) are not applied to components that are hidden by an `if` expression - hidden components will never be included in the annotation output, even if they would be considered "required" had they been visible.

Components can also be made conditional on properties of the _document_, or a combination of the document and the annotation values, for example

<AnnotationRendererPreview :config="configs.configConditional2" :document="configs.docsConditional2" pre-annotation="preanno">

**Project configuration**

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
        "options": [
            {"value": "negative", "label": "Negative"},
            {"value": "neutral", "label": "Neutral"},
            {"value": "positive", "label": "Positive"}
        ]
    },
    {
        "name": "reason",
        "type": "text",
        "title": "Why do you disagree with the suggested value?",
        "if": "annotation.sentiment !== document.preanno.sentiment"
    }
]
```

**Documents**

```json
[
    {
        "text": "I love the thing!",
        "preanno": { "sentiment": "positive" }
    },
    {
        "text": "I hate the thing!",
        "preanno": { "sentiment": "negative" }
    },
    {
        "text": "The thing is ok, I guess...",
        "preanno": { "sentiment": "neutral" }
    }
]
```

</AnnotationRendererPreview>

The full list of supported constructions is as follows:

- the `annotation` variable refers to the current state of the annotation components for this document
  - the current value of a particular component can be accessed as `annotation.componentName` or `annotation['component name']` - the brackets version will always work, the dot version works if the component's `name` is a valid JavaScript identifier
  - if a component has not been set since the form was last cleared the value may be `null` or `undefined` - the expression should be written to cope with both
  - the value of a `text`, `textarea`, `radio` or `selector` component will be a single string (or null/undefined), the value of a `checkbox` component will be an _array_ of strings since more than one value may be selected.  If no value is selected the array may be null, undefined or empty, the expression must be prepared to handle any of these
- the `document` variable refers to the current document that is being annotated
  - again properties of the document can be accessed as `document.propertyName` or `document['property name']`
  - continue the same pattern for nested properties e.g. `document.scores.label1`
  - individual elements of array properties can be accessed by zero-based index (e.g. `document.options[0]`)
- various comparison operators are available:
  - `==` and `!=` (equal and not-equal)
  - `<`, `<=`, `>=`, `>` (less-than, less-or-equal, greater-or-equal, greater-than)
    - these operators follow JavaScript rules, which are not always intuitive.  Generally if both arguments are strings then they will be compared by lexicographic order, but if either argument is a number then the other one will also be converted to a number before comparing.  So if the `score` component is set to the value "10" (a string of two digits) then `annotation.score < 5` would be _false_ (10 is converted to number and compared to 5) but `annotation.score < '5'` would be _true_ (the string "10" sorts before the string "5")
  - `in` checks for the presence of an item in an array or a key in an object
    - e.g. `'other' in annotation.someCheckbox` checks if the `other` option has been ticked in a checkbox component (whose value is an array)
    - this is different from normal JavaScript rules, where `i in myArray` checks for the presence of an array _index_ rather than an array _item_
- other operators
  - `+` (concatenate strings, or add numbers)
    - if either argument is a string then both sides are converted to strings and concatenated together
    - otherwise both sides are treated as numbers and added
  - `-`, `*`, `/`, `%` (subtraction, multiplication, division and remainder)
  - `&&`, `||` (boolean AND and OR)
  - `!` (prefix boolean NOT, e.g. `!annotation.selected` is true if `selected` is false/null/undefined and false otherwise)
  - conditional operator `expr ? valueIfTrue : valueIfFalse` (exactly as in JavaScript, first evaluates the test `expr`, then either the `valueIfTrue` or `valueIfFalse` depending on the outcome of the test)
- `value =~ /regex/` tests whether the given string value contains any matches for the given [regular expression](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions#writing_a_regular_expression_pattern)
  - use `^` and/or `$` to anchor the match to the start and/or end of the value, for example `annotation.example =~ /^a/i` checks whether the `example` annotation value _starts with_ "a" or "A" (the `/i` flag makes the expression case-insensitive)
  - since the project configuration is entered as JSON, any backslash characters within the regex must be doubled to escape them from the JSON parser, i.e. `"if": "annotation.option =~ /\\s/"` would check if `option` contains any space characters (for which the regular expression literal is `/\s/`)
- _Quantifier_ expressions let you check whether `any` or `all` of the items in an array or key/value pairs in an object match a predicate expression.  The general form is `any(x in expr, predicate)` or `all(x in expr, predicate)`, where `expr` is an expression that resolves to an array or object value, `x` is a new identifier, and `predicate` is the expression to test each item against.  The `predicate` expression can refer to the `x` identifier
  - `any(option in annotation.someCheckbox, option > 3)`
  - `all(e in document.scores, e.value < 0.7)` (assuming `scores` is an object mapping labels to scores, e.g. `{"scores": {"positive": 0.5, "negative": 0.3}}`)
    - when testing a predicate against an _object_ each entry has `.key` and `.value` properties giving the key and value of the current entry
  - on a null, undefined or empty array/object, `any` will return _false_ (since there are no items that pass the test) and `all` will return _true_ (since there are no items that _fail_ the test)
  - the predicate is optional - `any(arrayExpression)` resolves to `true` if any item in the array has a value that JavaScript considers to be "truthy", i.e. anything other than the number 0, the empty string, null or undefined.  So `any(annotation.myCheckbox)` is a convenient way to check whether _at least one_ option has been selected in a `checkbox` component. 

If the `if` expression for a particular component is _syntactically invalid_ (missing operands, mis-matched brackets, etc.) then the condition will be ignored and the component will always be displayed as though it did not have an `if` expression at all.  Conversely, if the expression is valid but an error occurs while _evaluating_ it, this will be treated the same as if the expression returned `false`, and the associated component will not be displayed.  The behaviour is this way around as the most common reason for errors during evaluation is attempting to refer to annotation components that have not yet been filled in - if this is not appropriate in your use case you must account for the possibility within your expression.  For example, suppose `confidence` is a `radio` or `selector` component with values ranging from 1 to 5, then another component that declares

```
"if": "annotation.confidence && annotation.confidence < 4"`
```

will hide this component if `confidence` is unset, displaying it only if `confidence` is set to a value less than 4, whereas

```
"if": "!annotation.confidence || annotation.confidence < 4"
```

will hide this component only if `confidence` is actually _set_ to a value of 4 or greater - it will _show_ this component if `confidence` is unset.  Either approach may be correct depending on your project's requirements.

To assist managers in authoring project configurations with `if` conditions, the "preview" mode on the project configuration page will display details of any errors that occur when parsing the expressions, or when evaluating them against the **Document input preview** data.  You are encouraged to test your expressions thoroughly against a variety of inputs to ensure they behave as intended, before opening your project to annotators.

<script>
import configs from './config_examples';
export default {
  computed: {
    configs(){ return configs }
  }

}
</script>
