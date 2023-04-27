/**
 * Script for building the index page after vite builds as the name of main .js and .css are hashed and changes
 * with every build.
 *
 * Takes the template from ./base_index.mustache, combine it with paths in ./dist/manifest.json to generate ./templates/index.html
 */

const fs = require("fs")
const path = require("path")
const _ = require("lodash")

let mainJsPath = ""
let mainCssPath = ""
try{
    const manifest = require("./dist/manifest.json")
    mainJsPath = manifest["src/main.js"].file
    mainCssPath = manifest["src/main.js"].css
}catch (e) {
    //manifest.json will only be created after frontend is built
    //so we use blank values for the js and css include paths otherwise
}


try{
    // Gets the base template
    const baseTemplate = fs.readFileSync("./base_index.html", "utf-8")

    // Provide mustache with context values from the manifest
    const context = {
        "main_js": mainJsPath,
        "main_css": mainCssPath,
    }

    // Render and save it to templates/index.html
    let outputHtmlTemplate = _.template(baseTemplate)
    let outputHtml = outputHtmlTemplate(context)
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




