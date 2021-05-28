export function generateBVOptions(options) {
    let optionsList = []
    for (let optionKey in options) {
        optionsList.push({
            value: optionKey,
            text: options[optionKey]
        })
    }

    return optionsList
}

/**
 *
 * @param file The file object obtained from DOM file upload input
 * @returns {Promise<unknown>}
 */
export async function readFileAsync(file){
    return  new Promise(resolve => {
        const reader = new FileReader()
        reader.onload = function (e) {
          resolve(e.target.result)
        }
        reader.readAsText(file)
    })

}


