# GATE Teamware Overview

## User roles

There are three types of users in GATE Teamware, [annotators](#annotators), [managers](#managers) 
and [admins](#admins). 

### Annotators

Annotator is the default role when signing up to Teamware. An annotator can be recruited into 
annotation projects and annotate documents. 


### Managers

Managers can create, view and modify annotation projects. They can also recruit annotators to a project.

### Admins

Admins, on top of what managers can do, they can also manage the users in the system and elevate them as
managers or admins.

## Annotation Projects, Documents and Annotations

Projects, documents and annotations form the core of the application.

### Projects

An annotation project contains a configuration of how annotations are to be captured, the documents and its
annotations and the recruited annotators.


### Documents

A document in application refers to an individual set of arbitrary text that's to be annotated. A document 
is stored as arbitrary JSON object and can represent various things such as, a single post (e.g. a tweet 
or a post from reddit), a pair of source post and reply or a part of a HTML web page.


### Annotations

An annotation represents a single annotation task against a single document. Like the document,
an annotation is stored as an arbitrary JSON object and can have any arbitrary structure.


