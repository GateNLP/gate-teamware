# Annotation Project Management

## Project Listing
Clicking on the `Projects` link in the top navigation bar takes you to a contains a list of existing 
projects. The project names are shown along with their summaries. Clicking on a project name will 
take you to the project management page.


## Project Management Page

The project management page contains all the functionalities to manage an annotation project. The page 
is composed of three main tabs:

* [Configuration](project_config.md) - Configure project settings including what annotations are captured.
* [Documents & Annotation](documents_annotations_management.md) - Manage documents and annotations. Upload documents, see contents of a document's annotations and import/export documents.
* [Annotators](annotators_management.md) - Manage the recruitment of annotators.

::: warning

Annotators can only be recruited to an annotation project after it has been configured and documents 
are uploaded to the project.

:::


## Project status icons
In the **Project listing** and **Project management page**, icon badges are used to provide a quick overview of the project's status: 

* <b-badge variant="success" class="mr-2" title="Completed annotations"><b-icon-pencil-fill></b-icon-pencil-fill>1</b-badge> - Number of completed annotations in the project.
* <b-badge variant="danger" class="mr-2" title="Rejected annotations"><b-icon-x-square-fill></b-icon-x-square-fill>1</b-badge> - Number of rejected annotations in the project.
* <b-badge variant="warning" class="mr-2" title="Timed out annotations"><b-icon-clock></b-icon-clock>1</b-badge> - Number of timed out annotations in the project.
* <b-badge variant="secondary" class="mr-2" title="Aborted annotations"><b-icon-stop-fill></b-icon-stop-fill>1</b-badge> - Number of aborted annotations in the project.
* <b-badge variant="primary" class="mr-2" title="Pending annotations"><b-icon-play-fill></b-icon-play-fill>1</b-badge> - Number of pending annotations in the project.
* <b-badge variant="dark" class="mr-2" title="Occupied (completed & pending)/Total tasks"><b-icon-card-checklist></b-icon-card-checklist>2/60</b-badge> - Number of occupied annotation tasks over number of total tasks in the project.
* <b-badge variant="info" class="mr-2" title="Number of documents"><b-icon-file-earmark-fill></b-icon-file-earmark-fill>20/5/10</b-badge> - Number of documents, training documents and test documents in the project.
* <b-badge variant="primary" class="mr-2" title="Number of current annotators. Annotators are removed from the project when they have completed all annotation tasks in their quota."><b-icon-person-fill></b-icon-person-fill>1</b-badge> - Number of annotators recruited in the project. Annotators are removed from the project when they have completed all annotation tasks in their quota.


