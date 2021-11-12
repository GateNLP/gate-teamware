# Documents & Annotations

The **Documents & Annotations** tab in the **Project management** page allows the viewing and management of documents
and annotations related to the project.

## Deleting documents and annotations

It is possible to click on the top left of corner of documents and annotations to select it, then click on the 
**Delete** button to delete them.

::: tip

Selecting a document also selects all its associated annotations.

:::

## Importing documents

Documents can be imported using the **Import** button. The supported file types are:

* `.json` - The app expects a list of documents (represented as a dictionary object) e.g. `[{"text": "Text1"}, ...]`.
* `.jsonl` - The app expects one document (represented as a dictionary object) per line.
* `.csv` - File must have a header row. It will be internally converted to JSON format.
* `.zip` - Can contain any number of `.json,.jsonl and .csv` files inside.


## Exporting documents

Documents and annotations can be exported using the **Export** button. A zip file is generated containing files
with 500 documents each. You can choose how documents are exported:

* `.json` & `.jsonl` - JSON or JSON Lines files can be generated in the format of:
  * `raw` - Exports unmodified JSON. An additional field named `annotation_sets` is added for storing annotations. If you've originally uploaded in GATE format then choose this option.
  * `gate` -  Convert documents to GATE JSON format and export. A `name` field is added that takes the ID value from the ID field specified in the project configuration. Fields apart from `text` and the ID field specified in the project config are placed in the `features` field. An `annotation_sets` field is added for storing annotations.
* `.csv` - The JSON documents will be flattened to csv's column based format. Annotations are added as additional columns with the header of `annotations.username.label`.
