# Documents & Annotations

The **Documents & Annotations** tab in the **Project management** page allows the viewing and management of documents
and annotations related to the project.

## Document & Annotation status

### Annotation status
Annotations can be in 1 of 5 states:

* <b-badge variant="success" class="mr-2" title="Completed annotations"><b-icon-pencil-fill></b-icon-pencil-fill></b-badge> <strong>Annotation is completed</strong> - The annotator has completed this annotation task.
* <b-badge variant="danger" class="mr-2" title="Rejected annotations"><b-icon-x-square-fill></b-icon-x-square-fill></b-badge> <strong>Annotation is rejected</strong> - The annotator has chosen to not annotate the document.
* <b-badge variant="warning" class="mr-2" title="Timed out annotations"><b-icon-clock></b-icon-clock></b-badge> <strong>Annotation is timed out</strong> - The annotation task was not completed within the time specified in the project's configuration. The task is freed and can be assigned to another annotator.
* <b-badge variant="secondary" class="mr-2" title="Aborted annotations"><b-icon-stop-fill></b-icon-stop-fill></b-badge> <strong>Annotation is aborted</strong> - The annotation task was aborted due to reasons other than timing out, such as when an annotator with a pending task is removed from a project.
* <b-badge variant="primary" class="mr-2" title="Pending annotations"><b-icon-play-fill></b-icon-play-fill></b-badge> <strong>Annotation is pending</strong> - The annotator has started the annotation task but has not completed it.

### Document status
Documents also display a list of its current annotation status: 

* <b-badge variant="success" class="mr-2" title="Completed annotations"><b-icon-pencil-fill></b-icon-pencil-fill>1</b-badge> - Number of completed annotations in the document.
* <b-badge variant="danger" class="mr-2" title="Rejected annotations"><b-icon-x-square-fill></b-icon-x-square-fill>1</b-badge> - Number of rejected annotations in the document.
* <b-badge variant="warning" class="mr-2" title="Timed out annotations"><b-icon-clock></b-icon-clock>1</b-badge> - Number of timed out annotations in the document.
* <b-badge variant="secondary" class="mr-2" title="Aborted annotations"><b-icon-stop-fill></b-icon-stop-fill>1</b-badge> - Number of aborted annotations in the document.
* <b-badge variant="primary" class="mr-2" title="Pending annotations"><b-icon-play-fill></b-icon-play-fill>1</b-badge> - Number of pending annotations in the document.

## Importing documents

Documents can be imported using the **Import** button. The supported file types are:

* `.json` - The app expects a list of documents (represented as a dictionary object) e.g. `[{"id": 1, "text": "Text1"}, ...]`.
* `.jsonl` - The app expects one document (represented as a dictionary object) per line.
* `.csv` - File must have a header row. It will be internally converted to JSON format.
* `.zip` - Can contain any number of `.json,.jsonl and .csv` files inside.

### Importing Training and Test documents

When importing documents for the training and testing phase, Teamware expects a field/column (called `gold` by default) 
that contains the correct annotation response for each label and, only for training documents, an explanation.

For example, if we're expecting a multi-choice label for doing sentiment classification with a 
widget named `sentiment` and choice of `postive`, `negative` and `neutrual`:

```js
[
    {
        "text": "What's my sentiment",
        "gold": {
            "sentiment": {
                "value": "positive", // For this document, the correct value is postive
                "explanation": "Because..." // Explanation is only given in the traiing phase and are optional in the test documents
            }
        }
    }
]
```

in csv:

| text | gold.sentiment.value | gold.sentiment.explanation |
| --- | --- | --- |
| What's my sentiment | positive | Because... |



### Guidance on CSV column headings

It is recommended that:

* Spaces are not used in column headings, use dash (`-`), underscore (`_`) or camel case (e.g. fieldName) instead.
* The `.` is used to indicate hierachical information so don't use it if that's not what's intended. 
  Explanation on this feature is given below.
  
Documents imported from a CSV files are converted to JSON for use internally in Teamware, the reverse is true 
when converting back to CSV. To allow a CSV to represent a tree structure, a dot notation is used to indicate
a sub-field. 

In the following example, we can see that `gold` has a child field named `sentiment` which then has a child
field named `value`:

| text | gold.sentiment.value | gold.sentiment.explanation |
| --- | --- | --- |
| What's my sentiment | positive | Because... |

The above column headers will generate the following JSON:

```js
[
    {
        "text": "What's my sentiment",
        "gold": {
            "sentiment": {
                "value": "positive", // For this document, the correct value is postive
                "explanation": "Because..." // Explanation is only given in the traiing phase and are optional in the test documents
            }
        }
    }
]
```


 

## Exporting documents

Documents and annotations can be exported using the **Export** button. A zip file is generated containing files
with 500 documents each. You can choose how documents are exported:

* `.json` & `.jsonl` - JSON or JSON Lines files can be generated in the format of:
  * `raw` - Exports unmodified JSON. If you've originally uploaded in GATE format then choose this option.
  
    An additional field named `annotation_sets` is added for storing annotations. The annotations are laid out 
    in the same way as GATE JSON format. For example if a document has been annotated by `user1` with labels and values
    `text`:`Annotation text`, `radio`:`val3`, and `checkbox`:`["val2", "val4"]`:
  
    ```json
    {
      "id": 32,
      "text": "Document text",
      "text2": "Document text 2",
      "feature1": "Feature text",
      "annotation_sets":{
        "user1":{
           "name":"user1",
           "annotations":[
              {
                 "type":"Document",
                 "start":0,
                 "end":10,
                 "id":0,
                 "features":{
                    "label":{
                       "text":"Annotation text",
                       "radio":"val3",
                       "checkbox":[
                          "val2",
                          "val4"
                       ]
                    }
                 }
              }
           ],
           "next_annid":1
        }
      }
    }
    ```
    
  * `gate` -  Convert documents to GATE JSON format and export. A `name` field is added that takes the ID value from the ID field specified in the project configuration. Fields apart from `text` and the ID field specified in the project config are placed in the `features` field. An `annotation_sets` field is added for storing annotations.
    
    For example in the case of this uploaded JSON document:
    ```json
    {
      "id": 32,
      "text": "Document text",
      "text2": "Document text 2",
      "feature1": "Feature text"
    }
    ```
    The generated output is as follows. The annotations are formatted same as the `raw` output above:
    ```json
    {
      "name": 32,
      "text": "Document text",
      "features": {
        "text2": "Document text 2",
        "feature1": "Feature text"
      },
      "offset_type":"p",
      "annotation_sets": {...}
    }
    ```
* `.csv` - The JSON documents will be flattened to csv's column based format. Annotations are added as additional columns with the header of `annotations.username.label`.

## Deleting documents and annotations

It is possible to click on the top left of corner of documents and annotations to select it, then click on the 
**Delete** button to delete them.

::: tip

Selecting a document also selects all its associated annotations.

:::
