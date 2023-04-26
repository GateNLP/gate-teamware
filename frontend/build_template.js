/**
 * Script for building the index page after vite builds as the name of main .js and .css are hashed and changes
 * with every build.
 *
 * Takes the template from ./base_index.mustache, combine it with paths in ./dist/manifest.json to generate ./templates/index.html
 */

const fs = require("fs")
const path = require("path")
const mustache = require("mustache")
const manifest = require("./dist/manifest.json")

try{
    // Gets the base template
    const baseTemplate = fs.readFileSync("./base_index.mustache", "utf-8")

    // Provide mustache with context values from the manifest
    const context = {
        "main_js": manifest["src/main.js"].file,
        "main_css": manifest["src/main.js"].css,
        // also supply the strings "{{" and "}}" as variables, so we can output Django template
        // placeholders without having them interpreted by Mustache on the way.
        "open_braces": "{{",
        "close_braces": "}}",
    }

    // Render and save it to templates/index.html
    let outputHtml = mustache.render(baseTemplate, context)
    const templateDir = "templates"
    if(!fs.existsSync(templateDir))
        fs.mkdirSync(templateDir)
    const outputHtmlPath = path.join(templateDir, "index.html")
    fs.writeFileSync(outputHtmlPath, outputHtml)
    console.log("Generated index.html at " +outputHtmlPath)

}catch (e) {
    console.log("Could not generate index.html")
    console.log(e)
}




