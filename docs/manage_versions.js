const fs = require("fs")
const path = require("path")
const {execSync} = require("child_process")
const docs_config = require("./docs.config")


/**
 *
 * @type {string}
 */
const VERSIONS_JSON_PATH = ".vuepress/versions.json"


/**
 * Reads a JSON file from filePath and returns the parsed object
 * @param filePath Location of the JSON file
 * @returns {any} Object parsed in the JSON file
 */
function readJsonFileSync(filePath){
    if(fs.existsSync(filePath) && fs.lstatSync(filePath).isFile()){
        return JSON.parse(fs.readFileSync(filePath))
    }else{
        throw new Error(`File ${filePath} does not exist or is a directory.`)
    }
}


/**
 * Converts an object to JSON string and writes to filePath
 * @param filePath Location to save the JSON file
 * @param content Object to save
 */
function writeJsonFileSync(filePath, content){
    fs.writeFileSync(filePath, JSON.stringify(content, null, " "))

}

/**
 * Save the current version of the documentation and give it a version number.
 * @param docsDir Directory of the current documentation.
 * @param versionedDir Directory containing all versioned documentation.
 * @param versionNumber The version number to use.
 */
function createDocumentationVersion(docsDir, versionedDir, versionNumber) {

    console.log(`Saving new documentation version ${versionNumber}. Documentation files are located at ${docsDir}, and version will be archived at ${versionedDir}.`)

    if(!fs.existsSync(docsDir)){
        throw new Error(`Documentation directory "${docsDir}" does not exist`)
    }

    // Create a directory to hold the documentation versions if it doesn't exist
    const new_doc_version_path = path.join(versionedDir, versionNumber)
    if (!fs.existsSync(new_doc_version_path)) {

        fs.mkdirSync(new_doc_version_path, {recursive: true})

        //Copy the files to the version directory
        fs.cpSync(docsDir, new_doc_version_path, {recursive: true})
    } else {
        throw new Error(`Version ${versionNumber} already exists.`)
    }

}

/**
 * Update all versions.json in both the latest documentation and the versioned documentation
 * @param docsDir Directory of the current documentation.
 * @param versionedDocsDir Directory containing all versioned documentation.
 * @param basePath Root path of the documentation site.
 * @param frontendSourceDir Directory where the frontend's source code is located, allows the documentation to use frontend's components.
 * @param latestVersionName Name to use for the unversioned (latest) documentation.
 */
function updateVersionsListing(docsDir, versionedDocsDir, basePath, frontendSourceDir, latestVersionName = "latest") {

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

    // Build a list of all versions
    let all_versions = [...versions, {text: latestVersionName, value: basePath+latestVersionName+"/"}]

    // Update source directory
    let src_versions_json = {
        current: latestVersionName,
        base: basePath+latestVersionName+"/",
        versions: all_versions,
        frontendSource: path.relative(path.join(docsDir, ".vuepress"), frontendSourceDir)
    }
    writeJsonFileSync(path.join(docsDir, VERSIONS_JSON_PATH), src_versions_json)

    // Update versioned directories
    versions.forEach(version => {
        let version_json = {
            current: version.text,
            base: version.value,
            versions: all_versions,
            frontendSource: path.relative(path.join(versionedDocsDir, version.text, ".vuepress"), frontendSourceDir)
        }
        writeJsonFileSync(path.join(versionedDocsDir, version.text, VERSIONS_JSON_PATH), version_json)
    })

    console.log("Updated versions.json for")
    all_versions.forEach(av => {
        console.log(`Version name ${av.text} with base path ${av.value}`)
    })
}


/**
 * Builds the documentation site.
 * @param docsDir Directory of the current documentation.
 * @param versionedDocsDir Directory containing all versioned documentation.
 * @param targetDir Directory where the site will be built to.
 * @param defaultVersionName The default version of the documentation that will be displayed.
 */
function buildDocumentation(docsDir, versionedDocsDir, targetDir, defaultVersionName = null) {
    // Gets all the versions
    let versionNames = []
    fs.readdirSync(versionedDocsDir, {withFileTypes: true}).forEach(content => {
        if (content.isDirectory()) {
            versionNames.push(content.name)
        }
    })

    // Creates target directory
    fs.mkdirSync(targetDir, {recursive: true})


    const latestVersionData = readJsonFileSync(path.join(docsDir,  VERSIONS_JSON_PATH))
    console.log(`Building latest version: ${latestVersionData.current}`)
    execSync(`vuepress build -d ${path.join(targetDir,"development")} ${docsDir}`)

    let versionsData = []
    versionNames.forEach(versionName =>{
        const versionData = readJsonFileSync(path.join(versionedDocsDir, versionName, VERSIONS_JSON_PATH))
        console.log(`Building version: ${versionData.current}`)
        versionsData.push(versionData)
        execSync(`vuepress build -d ${path.join(targetDir,versionName)} ${path.join(versionedDocsDir, versionName)}`)
    })

    console.log("Finished building")

    if( defaultVersionName == null){
        // Makes latest version the default version
        defaultVersionName = latestVersionData.current
    } else {
        // Check that the version exists
        let versionExist = false
        if(latestVersionData.current === defaultVersionName)
            versionExist = true

        versionsData.forEach(vData => {
            if(vData.current === defaultVersionName){
                versionExist = true
            }
        })

        if(!versionExist){
            console.log(`Specified version ${defaultVersionName} to use as a default does not exist. Using the latest version instead ${latestVersionData.current}.`)
            defaultVersionName = latestVersionData.current
        }
    }

    // Make a redirect page to the default version
    let redirectPageContents = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="Refresh" content="0; url='${defaultVersionName}'" />
        </head>
        <body>
            <p>
                Go the documentation website here if you were not redirected automatically: <a href="${defaultVersionName}">GATE Teamware Documentation</a>
            </p>
        </body>
        </html>`
    fs.writeFileSync(path.join(targetDir,"index.html"), redirectPageContents)

}

function main(){
    try{
        const command = process.argv[2]
        if(command){
            if(command === "create"){
                const version = process.argv[3]
                if(version){
                    createDocumentationVersion(docs_config.documentationDir,
                        docs_config.documentationVersionsDir,
                        version)
                    updateVersionsListing(docs_config.documentationDir,
                        docs_config.documentationVersionsDir,
                        docs_config.base,
                        docs_config.frontendSourceDir,
                        docs_config.latestVersionName)
                    return 0
                }

            }else if(command === "update"){
                updateVersionsListing(docs_config.documentationDir,
                    docs_config.documentationVersionsDir,
                    docs_config.base,
                    docs_config.frontendSourceDir,
                    docs_config.latestVersionName)
                return 0

            }else if(command === "build"){
                buildDocumentation(docs_config.documentationDir,
                    docs_config.documentationVersionsDir,
                    docs_config.buildTargetDir,
                    docs_config.defaultVersion)
                return 0

            }else{
                console.log("Command not recognised.\n")
            }
        }
    }catch (e){
        console.log(e)
        return 0
    }



    // Print instructions by default
    console.log(`Use the following commands with manage_versions.js:
    manage_versions.js create version_number - Creates a new version using version_number
    manage_versions.js update - Update version listing (versions.json) files
    manage_versions.js build - Builds the documentation site
    
    Configuration parameters can be found in docs.config.js.`)
    return 1

}
return main()
