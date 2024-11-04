(window.webpackJsonp=window.webpackJsonp||[]).push([[18],{316:function(t,e,s){"use strict";s.r(e);var a=s(16),n=Object(a.a)({},(function(){var t=this,e=t._self._c;return e("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[e("h1",{attrs:{id:"frontend"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#frontend"}},[t._v("#")]),t._v(" Frontend")]),t._v(" "),e("p",[t._v("Web GUI of Teamware is built with "),e("a",{attrs:{href:"https://vuejs.org",target:"_blank",rel:"noopener noreferrer"}},[t._v("vue.js"),e("OutboundLink")],1),t._v(" version 2.7.x.")]),t._v(" "),e("p",[e("a",{attrs:{href:"https://getbootstrap.com/",target:"_blank",rel:"noopener noreferrer"}},[t._v("Bootstrap"),e("OutboundLink")],1),t._v(" (and "),e("a",{attrs:{href:"https://bootstrap-vue.org/",target:"_blank",rel:"noopener noreferrer"}},[t._v("Bootstrap vue"),e("OutboundLink")],1),t._v(") provides the visual styling.")]),t._v(" "),e("p",[e("a",{attrs:{href:"https://vitejs.dev/",target:"_blank",rel:"noopener noreferrer"}},[t._v("Vite.js"),e("OutboundLink")],1),t._v(" is used to bundle Vue code and other javascript dependencies for deployment and serve as a frontend dev server (which runs alongside django dev server) while testing or debugging.")]),t._v(" "),e("h2",{attrs:{id:"getting-started"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#getting-started"}},[t._v("#")]),t._v(" Getting started")]),t._v(" "),e("h3",{attrs:{id:"installation"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#installation"}},[t._v("#")]),t._v(" Installation")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm install\n")])])]),e("h3",{attrs:{id:"compiles-and-hot-reloads-for-development"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#compiles-and-hot-reloads-for-development"}},[t._v("#")]),t._v(" Compiles and hot-reloads for development")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm run serve\n")])])]),e("h3",{attrs:{id:"compiles-and-minifies-for-production"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#compiles-and-minifies-for-production"}},[t._v("#")]),t._v(" Compiles and minifies for production")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm run build\n")])])]),e("h3",{attrs:{id:"testing"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#testing"}},[t._v("#")]),t._v(" Testing")]),t._v(" "),e("p",[e("strong",[t._v("Tools used for testing:")])]),t._v(" "),e("ul",[e("li",[e("p",[e("a",{attrs:{href:"https://vitest.dev",target:"_blank",rel:"noopener noreferrer"}},[t._v("vitest"),e("OutboundLink")],1),t._v(" - Used for unit testing (code without UI components)")])]),t._v(" "),e("li",[e("p",[e("a",{attrs:{href:"https://docs.cypress.io",target:"_blank",rel:"noopener noreferrer"}},[t._v("cypress"),e("OutboundLink")],1),t._v(" - Used for tests that contains (Vue) UI components")])]),t._v(" "),e("li",[e("p",[e("a",{attrs:{href:"https://vue-test-utils.vuejs.org",target:"_blank",rel:"noopener noreferrer"}},[t._v("Vue test utils"),e("OutboundLink")],1),t._v(" - Used for rendering vue component allows it to be mounted for unit testing. Officially recommended by Vue.js.")])]),t._v(" "),e("li",[e("p",[t._v("Tests for the frontend are all located in "),e("code",[t._v("/frontend/tests")]),t._v(" folder.")]),t._v(" "),e("ul",[e("li",[t._v("Unit test files should all be placed in "),e("code",[t._v("/frontend/tests/unit/")]),t._v(" folder and have an extension "),e("code",[t._v(".spec.js")]),t._v(".")]),t._v(" "),e("li",[t._v("Component test files should all be placed in "),e("code",[t._v("/frontend/tests/component")]),t._v(" folder and have an extension "),e("code",[t._v(".cy.js")])])])]),t._v(" "),e("li",[e("p",[t._v("Test fixtures (data used in running the tests) are placed in "),e("code",[t._v("/examples")]),t._v(" folder, this folder is shared with the integration test")])])]),t._v(" "),e("p",[t._v("To run all frontend tests (unit and component tests):")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm run test\n")])])]),e("p",[t._v("To run unit tests only:")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm run test:unit\n")])])]),e("p",[t._v("To run component test only:")]),t._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[t._v("npm run test:component\n")])])]),e("h2",{attrs:{id:"notes-when-coming-from-the-previous-version-2-0-0"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#notes-when-coming-from-the-previous-version-2-0-0"}},[t._v("#")]),t._v(" Notes when coming from the previous version <=2.0.0")]),t._v(" "),e("ul",[e("li",[t._v("The "),e("code",[t._v("@")]),t._v(" alias can still be used when doing module imports but file extensions should now be used when importing "),e("code",[t._v(".vue")]),t._v(" files e.g.\n"),e("ul",[e("li",[t._v('Before: `import DeleteModal from "@/components/DeleteModal"')]),t._v(" "),e("li",[t._v("Now:  "),e("code",[t._v('import DeleteModal from "@/components/DeleteModal.vue"')])])])]),t._v(" "),e("li",[t._v("For code that is intended to run on the browser, e.g. in all "),e("code",[t._v(".vue")]),t._v(" files, imports should use the ES 6 compliant "),e("code",[t._v("import")]),t._v("  command and not node/commonjs's "),e("code",[t._v("require")]),t._v(" "),e("ul",[e("li",[e("strong",[t._v("Exceptions for code that is run directly by node")]),t._v(", e.g. scripts used in the build chain, config files and test files used by build tools that run on node (e.g. vuepress or cypress)")])])])]),t._v(" "),e("h2",{attrs:{id:"explantion-of-the-frontend"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#explantion-of-the-frontend"}},[t._v("#")]),t._v(" Explantion of the frontend")]),t._v(" "),e("h3",{attrs:{id:"vue-and-vite"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#vue-and-vite"}},[t._v("#")]),t._v(" Vue and Vite")]),t._v(" "),e("p",[t._v("Instead of separating html, css and javascript files, Vue has its own "),e("code",[t._v("single-file component")]),t._v(" format normally with "),e("code",[t._v(".vue")]),t._v(" extension ("),e("a",{attrs:{href:"https://vuejs.org/guide/scaling-up/sfc.html",target:"_blank",rel:"noopener noreferrer"}},[t._v("reason why this file format is used"),e("OutboundLink")],1),t._v("). Here is an example "),e("code",[t._v(".vue")]),t._v(" file:")]),t._v(" "),e("div",{staticClass:"language-vue extra-class"},[e("pre",{pre:!0,attrs:{class:"language-vue"}},[e("code",[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("script")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),e("span",{pre:!0,attrs:{class:"token script"}},[e("span",{pre:!0,attrs:{class:"token language-javascript"}},[t._v("\n"),e("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("export")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("default")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n  "),e("span",{pre:!0,attrs:{class:"token function"}},[t._v("data")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n    "),e("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("return")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n      "),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("greeting")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token string"}},[t._v("'Hello World!'")]),t._v("\n    "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n  "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])]),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("script")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n\n"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("template")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n  "),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("p")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("class")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("greeting"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("{{ greeting }}"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("p")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("template")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n\n"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("style")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),e("span",{pre:!0,attrs:{class:"token style"}},[e("span",{pre:!0,attrs:{class:"token language-css"}},[t._v("\n"),e("span",{pre:!0,attrs:{class:"token selector"}},[t._v(".greeting")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n  "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v("color")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" red"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(";")]),t._v("\n  "),e("span",{pre:!0,attrs:{class:"token property"}},[t._v("font-weight")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" bold"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(";")]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])]),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("style")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n")])])]),e("p",[t._v("This means that "),e("code",[t._v(".vue")]),t._v(" files cannot be directly imported into a standard html page. A tool has to be used for converting "),e("code",[t._v(".vue")]),t._v(" file into standard javascript and/or css files, this is where "),e("a",{attrs:{href:"https://vitejs.dev/",target:"_blank",rel:"noopener noreferrer"}},[t._v("Vite.js"),e("OutboundLink")],1),t._v(" comes in.")]),t._v(" "),e("p",[e("a",{attrs:{href:"https://vitejs.dev/",target:"_blank",rel:"noopener noreferrer"}},[t._v("Vite.js"),e("OutboundLink")],1),t._v(" is a tool that, amongst many other things, provides a dev server allowing hot module replacement (ability to immediately see changes in the UI during development) and bundling of javascript modules and other resources (css, images, etc.) i.e. not having to individually import each javascript and their dependencies from the main page. A "),e("a",{attrs:{href:"https://github.com/vitejs/vite-plugin-vue2",target:"_blank",rel:"noopener noreferrer"}},[t._v("Vue plugin"),e("OutboundLink")],1),t._v(" is used to automatically convert "),e("code",[t._v(".vue")]),t._v(" files into plain javascript as part of the bundling process.")]),t._v(" "),e("h3",{attrs:{id:"app-entrypoint-main-js-and-routing"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#app-entrypoint-main-js-and-routing"}},[t._v("#")]),t._v(" App entrypoint (main.js) and routing")]),t._v(" "),e("p",[t._v("The application's main entrypoint is "),e("code",[t._v("/frontend/src/main.js")]),t._v(" which loads dependencies like Vue, Bootstrap Vue as well as loading the main component "),e("code",[t._v("AnnotationApp.vue")]),t._v(" into a html page that contains a "),e("code",[t._v('<div id="app"></div>')]),t._v(" tag.")]),t._v(" "),e("p",[t._v("The "),e("code",[t._v("AnnotationApp.vue")]),t._v(" component contains the special "),e("code",[t._v("<router-view></router-view>")]),t._v(" tag ("),e("a",{attrs:{href:"https://router.vuejs.org/",target:"_blank",rel:"noopener noreferrer"}},[t._v("vue router"),e("OutboundLink")],1),t._v(") which allows us to map url paths to specific vue components. The routing configuration can be found in "),e("code",[t._v("/frontend/src/router/index.js")]),t._v(", for example:")]),t._v(" "),e("div",{staticClass:"language-js extra-class"},[e("pre",{pre:!0,attrs:{class:"language-js"}},[e("code",[e("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("const")]),t._v(" routes "),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),t._v("\n    "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n        "),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("path")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token string"}},[t._v("'/'")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("name")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token string"}},[t._v("'Home'")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("component")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" Home"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("meta")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),e("span",{pre:!0,attrs:{class:"token literal-property property"}},[t._v("guest")]),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v(":")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token boolean"}},[t._v("true")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token operator"}},[t._v("...")]),t._v("\n")])])]),e("p",[t._v("The route shown above maps the root path e.g. "),e("code",[t._v("https://your-deployed-teamware-domain.com/")]),t._v(" to the "),e("code",[t._v("Home.vue")]),t._v(" component. Specifically, when pointing your browser to that path, the "),e("code",[t._v("Home.vue")]),t._v(" component is inserted inside "),e("code",[t._v("<router-view></router-view>")]),t._v(".")]),t._v(" "),e("h3",{attrs:{id:"index-html-templates-and-bundling"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#index-html-templates-and-bundling"}},[t._v("#")]),t._v(" index.html, templates and bundling")]),t._v(" "),e("p",[t._v("A html page is required to place our application in. Teamware uses Django to serve up the main html page which is located at "),e("code",[t._v("/frontend/templates/index.html")]),t._v(" (see "),e("code",[t._v("MainView")]),t._v(" class in "),e("code",[t._v("/backend/views.py")]),t._v("). This "),e("code",[t._v("index.html")]),t._v(" page has to know where to load the generated javascript files. Where these files are differ depending on whether you're running the vite development server or using vite's statically built files.")]),t._v(" "),e("h4",{attrs:{id:"using-vite-s-development-server-django-s-settings-frontend-dev-server-use-is-true"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#using-vite-s-development-server-django-s-settings-frontend-dev-server-use-is-true"}},[t._v("#")]),t._v(" Using vite's development server (Django's "),e("code",[t._v("settings.FRONTEND_DEV_SERVER_USE")]),t._v(" is "),e("code",[t._v("True")]),t._v(")")]),t._v(" "),e("p",[t._v("In during development we expect to be running the vite dev server alongside django server (when running "),e("code",[t._v("npm run serve")]),t._v(" from the root of the project). In this case "),e("code",[t._v("index.html")]),t._v(" imports javascript directly from the vite dev server:")]),t._v(" "),e("div",{staticClass:"language-html extra-class"},[e("pre",{pre:!0,attrs:{class:"language-html"}},[e("code",[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("script")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("type")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("module"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("src")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("http://localhost:5173/@vite/client"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),e("span",{pre:!0,attrs:{class:"token script"}}),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("script")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("script")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("type")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("module"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("src")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("http://localhost:5173/src/main.js"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),e("span",{pre:!0,attrs:{class:"token script"}}),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("script")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n")])])]),e("p",[t._v("This applies when running the "),e("code",[t._v("base")]),t._v(", "),e("code",[t._v("test")]),t._v(" and "),e("code",[t._v("integration")]),t._v(" django configurations.")]),t._v(" "),e("h4",{attrs:{id:"using-vite-s-statically-built-assets-django-s-settings-frontend-dev-server-use-is-false"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#using-vite-s-statically-built-assets-django-s-settings-frontend-dev-server-use-is-false"}},[t._v("#")]),t._v(" Using vite's statically built assets (Django's "),e("code",[t._v("settings.FRONTEND_DEV_SERVER_USE")]),t._v(" is "),e("code",[t._v("false")]),t._v(")")]),t._v(" "),e("p",[t._v("When deploying the application, vite converts "),e("code",[t._v(".vue")]),t._v(" files into plain javascript and bundles them to "),e("code",[t._v("/frontend/dist/static")]),t._v(" directory. The "),e("code",[t._v("/frontend/src/main.js")]),t._v(" becomes "),e("code",[t._v("/frontend/dist/static/assets/main-bb58d055.js")]),t._v(". The scripts are imported as static asset of going through the vite server, for example:")]),t._v(" "),e("div",{staticClass:"language-html extra-class"},[e("pre",{pre:!0,attrs:{class:"language-html"}},[e("code",[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("link")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("rel")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("stylesheet"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("href")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("/static/assets/main-89ece1f8.css"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),t._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("/>")])]),t._v("\n"),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("<")]),t._v("script")]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("type")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("module"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),t._v(" "),e("span",{pre:!0,attrs:{class:"token attr-name"}},[t._v("src")]),e("span",{pre:!0,attrs:{class:"token attr-value"}},[e("span",{pre:!0,attrs:{class:"token punctuation attr-equals"}},[t._v("=")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')]),t._v("/static/assets/main-bb58d055.js"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v('"')])]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),e("span",{pre:!0,attrs:{class:"token script"}}),e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token tag"}},[e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("</")]),t._v("script")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(">")])]),t._v("\n")])])]),e("p",[t._v("This applies when running the "),e("code",[t._v("deployment")]),t._v(", "),e("code",[t._v("docker-test")]),t._v(" and "),e("code",[t._v("docker-integration")]),t._v(" django configurations.")]),t._v(" "),e("h4",{attrs:{id:"index-html-generation"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#index-html-generation"}},[t._v("#")]),t._v(" index.html generation")]),t._v(" "),e("p",[t._v("You may have noticed that a hash is added to the generated asset files (e.g. "),e("code",[t._v("main-bb58d055.js")]),t._v(") and this hash changes every time Vite builds the code. This means the "),e("code",[t._v("index.html")]),t._v(" must also be re-generated after every Vite build as well.")]),t._v(" "),e("p",[t._v("A simple build script which runs after every vite build "),e("code",[t._v("/frontend/build_template.js")]),t._v(" performs this generation by taking the base template "),e("code",[t._v("/frontend/base_index.html")]),t._v(", merging it with Vite's generated manifest "),e("code",[t._v("/frontend/dist/manifest.json")]),t._v(" and the output with the correct import path to "),e("code",[t._v("/frontend/templates/index.html")]),t._v(".")])])}),[],!1,null,null,null);e.default=n.exports}}]);