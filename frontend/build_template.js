/**
 * Script for building the index page after vite builds as the name of main .js and .css are hashed and changes
 * with every build.
 *
 * Takes the template from ./base_index.html, combine it with paths in ./dist/manifest.json to generate ./templates/index.html
 */

import * as fs from "fs"
import * as path from "path"
import mustache from "mustache"
import manifest from "./dist/manifest.json" assert {type: "json"}

// Gets the base template
const baseTemplate = fs.readFileSync("./base_index.html", "utf-8")

// Provide mustache with context values from the manifest
const assetFiles = {
    "main_js": manifest["src/main.js"].file,
    "main_css": manifest["src/main.js"].css
}

// Render and save it to templates/index.html
let outputHtml = mustache.render(baseTemplate, assetFiles)
const templateDir = "templates"
if(!fs.existsSync(templateDir))
    fs.mkdirSync(templateDir)
fs.writeFileSync(path.join(templateDir, "index.html"), outputHtml)

