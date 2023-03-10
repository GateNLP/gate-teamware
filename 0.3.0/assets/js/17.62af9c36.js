(window.webpackJsonp=window.webpackJsonp||[]).push([[17],{414:function(e,t,n){"use strict";n.r(t);var o=n(53),a=Object(o.a)({},(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[n("h1",{attrs:{id:"managing-and-versioning-documentation"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#managing-and-versioning-documentation"}},[e._v("#")]),e._v(" Managing and versioning documentation")]),e._v(" "),n("p",[e._v("Documentation versioning is managed by the custom node script located at "),n("code",[e._v("docs/manage_versions.js")]),e._v(". Versions of the documentation can be archived and the entire documentation site can be built using the script.")]),e._v(" "),n("p",[e._v("Various configuration parameters used for management of documentation versioning can be found in "),n("code",[e._v("docs/docs.config.js")]),e._v(".")]),e._v(" "),n("h2",{attrs:{id:"editing-the-documentation"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#editing-the-documentation"}},[e._v("#")]),e._v(" Editing the documentation")]),e._v(" "),n("p",[e._v("The latest version of the documentation is located at "),n("code",[e._v("/docs/docs")]),e._v(". The archived (versioned) documentation are located in "),n("code",[e._v("/docs/versioned/version_number")]),e._v(".")]),e._v(" "),n("p",[e._v("Use the following command to live preview the latest version of the documentation:")]),e._v(" "),n("div",{staticClass:"language- extra-class"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[e._v("npm run serve:docs\n")])])]),n("p",[e._v("Note that this will not work with other versioned docs as they are managed as a separate site. To live preview versioned documentation use the command (replace version_num with the version you'd like to preview):")]),e._v(" "),n("div",{staticClass:"language- extra-class"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[e._v("vuepress dev docs/versioned/version_num\n")])])]),n("h2",{attrs:{id:"creating-a-new-documentation-version"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#creating-a-new-documentation-version"}},[e._v("#")]),e._v(" Creating a new documentation version")]),e._v(" "),n("p",[e._v("To create a version of the documentation, run the command:")]),e._v(" "),n("div",{staticClass:"language- extra-class"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[e._v("npm run docs:create_version\n")])])]),n("p",[e._v("This creates a copy of the current set of documentation in "),n("code",[e._v("/docs/docs")]),e._v(" and places it at "),n("code",[e._v("/docs/versioned/version_num")]),e._v(". The version number in "),n("code",[e._v("package.json")]),e._v(" is used for the documentation version.")]),e._v(" "),n("p",[e._v("Each set of documentation can be considered as a separate vuepress site. Each one has a "),n("code",[e._v(".vuepress/versions.json")]),e._v(" file that contains the listing of all versions, allowing them to link to each other.")]),e._v(" "),n("p",[e._v("Note: Versions can also be created manually by running the command:")]),e._v(" "),n("div",{staticClass:"language- extra-class"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[e._v("# Replace version_num with the version you'd like to create\nnode docs/manage_versions.js create version_num \n")])])]),n("h2",{attrs:{id:"building-documentation-site"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#building-documentation-site"}},[e._v("#")]),e._v(" Building documentation site")]),e._v(" "),n("p",[e._v("To build the documentation site, the previous documentation build command is used:")]),e._v(" "),n("div",{staticClass:"language- extra-class"},[n("pre",{pre:!0,attrs:{class:"language-text"}},[n("code",[e._v("npm run build:docs\n")])])]),n("h2",{attrs:{id:"implementation-of-the-version-selector-ui"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#implementation-of-the-version-selector-ui"}},[e._v("#")]),e._v(" Implementation of the version selector UI")]),e._v(" "),n("p",[e._v("A partial override of the default Vuepress theme was needed to add a custom component the navigation bar. The modified version of the "),n("code",[e._v("NavBar")]),e._v(" component can be found in "),n("code",[e._v("/docs/docs/.vuepress/theme/components/NavBar.vue")]),e._v(". The modified NavBar uses the "),n("code",[e._v("VersionSelector")]),e._v(" ("),n("code",[e._v("/docs/docs/.vuepress/theme/components/VersionSelector.vue")]),e._v(") component which reads from the "),n("code",[e._v(".vuepress/versions.json")]),e._v(" from each set of documentation.")])])}),[],!1,null,null,null);t.default=a.exports}}]);