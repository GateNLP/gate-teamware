# Managing and versioning documentation

Documentation versioning is managed by the custom node script located at `docs/manage_versions.js`. Versions of the documentation can be archived and the entire documentation site can be built using the script.

Various configuration parameters used for management of documentation versioning can be found in `docs/docs.config.js`.

## Editing the documentation

The latest version of the documentation is located at `/docs/docs`. The archived (versioned) documentation are located in `/docs/versioned/version_number`.

Use the following command to live preview the latest version of the documentation:

```
npm run serve:docs
```

Note that this will not work with other versioned docs as they are managed as a separate site. To live preview versioned documentation use the command (replace version_num with the version you'd like to preview):

```
vuepress dev docs/versioned/version_num
```

## Creating a new documentation version

To create a new documentation, run the following command and replacing `version_num` with the version number: 

```
npm run docs:create_version -- version_num
```

This creates a copy of the current set of documentation in `/docs/docs` and places it at `/docs/versioned/version_num`. 

Each set of documentation can be considered as a separate vuepress site. Each one has a `.vuepress/versions.json` file that contains the listing of all versions, allowing them to link to each other.  


## Building documentation site

To build the documentation site, the previous documentation build command is used:

```
npm run build:docs
```
