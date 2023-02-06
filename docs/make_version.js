const fs = require("fs")
const path = require("path")
const {execSync} = require("child_process")

const doc_src_dir = process.argv[2]
const doc_version_dir = process.argv[3]
const doc_version_create = process.argv[4]


if (!fs.existsSync(doc_src_dir)) {
    throw new Error("Documentation directory does not exist.")
}

if (!doc_version_dir) {
    throw new Error(("Destination is undefined"))
}

if (!doc_version_create) {
    throw new Error(("Version number is not defined"))
}

function createDocumentationVersion(docsDir, versionedDir, versionNumber) {

    console.log(`Saving new documentation version ${versionNumber}. Documentation files are located at ${docsDir}, and version will be archived at ${versionedDir}.`)

    // Create a directory to hold the documentation versions if it doesn't exist
    const new_doc_version_path = path.join(versionedDir, versionNumber)
    if (!fs.existsSync(new_doc_version_path)) {

        fs.mkdirSync(new_doc_version_path, {recursive: true})

        //Copy the files to the version directory
        fs.cpSync(docsDir, new_doc_version_path, {recursive: true})
    } else {
        throw new Error("Version already exists")
    }

}

/**
 * Update all versions.json
 * @param docsDir
 * @param versionedDocsDir
 * @param basePath
 * @param frontendSourceDir
 */
function updateVersionsListing(docsDir, versionedDocsDir, basePath, frontendSourceDir) {

    // Get all versioned directories
    let versions = []
    fs.readdirSync(versionedDocsDir, {withFileTypes: true}).forEach(content => {
        if (content.isDirectory()) {
            versions.push({
                text: content.name,
                value: basePath + content.name + "/"
            })
        }
    })
    const dev_version_name = "development"

    // Build a list of all versions
    let all_versions = [...versions, {text: dev_version_name, value: basePath+dev_version_name+"/"}]

    // Update source directory
    let src_versions_json = {
        current: dev_version_name,
        base: basePath+dev_version_name+"/",
        versions: all_versions,
        frontendSource: path.relative(path.join(docsDir, ".vuepress"), frontendSourceDir)
    }
    fs.writeFileSync(path.join(docsDir, ".vuepress/versions.json"), JSON.stringify(src_versions_json, null, " "))

    // Update versioned directories
    versions.forEach(version => {
        let version_json = {
            current: version.text,
            base: version.value,
            versions: all_versions,
            frontendSource: path.relative(path.join(versionedDocsDir, version.text, ".vuepress"), frontendSourceDir)
        }
        fs.writeFileSync(path.join(versionedDocsDir, version.text, ".vuepress/versions.json"), JSON.stringify(version_json, null, " "))
    })
}



function buildDocumentation(docsDir, versionedDocsDir, targetDir) {
    let versions = []
    fs.readdirSync(versionedDocsDir, {withFileTypes: true}).forEach(content => {
        if (content.isDirectory()) {
            versions.push(content.name)
        }
    })



    console.log("Building development version")
    execSync(`vuepress build -d ${path.join(targetDir,"development")} ${docsDir}`)


    versions.forEach(versionName =>{
        console.log("Building version "+versionName)
        execSync(`vuepress build -d ${path.join(targetDir,versionName)} ${path.join(versionedDocsDir, versionName)}`)
    })

    console.log("Finished building")

    // Make a redirect page to the default version (currently development)
    let redirectPageContents = `
        <html>
        <header>
            <meta http-equiv="Refresh" content="0; url='development'" />
        </header>
        <body>
            <p>
                Go the documentation website here if you were not redirected automatically: <a href="development">GATE Teamware Documentation</a>
            </p>
        </body>
        </html>`
    fs.writeFileSync(path.join(targetDir,"index.html"), redirectPageContents)

}

// createDocumentationVersion(doc_src_dir, doc_version_dir, doc_version_create)
// updateVersionsListing(doc_src_dir, doc_version_dir, "/gate-teamware/", "frontend/src")
buildDocumentation(doc_src_dir, doc_version_dir, "docs/site/gate-teamware/")

