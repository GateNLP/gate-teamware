const fs = require("fs")
const mustache = require("mustache")
const manifest = require("./dist/manifest.json")
const baseTemplate = fs.readFileSync("./base_index.html", "utf-8")
const templateFiles = {
    "main_js": manifest["src/main.js"].file,
    "main_css": manifest["src/main.js"].css
}
let outputHtml = mustache.render(baseTemplate, templateFiles)
fs.writeFileSync("templates/index.html", outputHtml)

