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

export async function showToast(vueOrComponentInstance, title, message, variant, delay = 3000){
    vueOrComponentInstance.$bvToast.toast(message, {
        title: title,
        toaster: 'b-toaster-top-full',
        variant: variant,
        autoHideDelay: delay,
        })
}

export async function toastSuccess(vueOrComponentInstance, title, message){
    await showToast(vueOrComponentInstance, title, message, "success")
}

export async function toastError(vueOrComponentInstance, title, message){
    await showToast(vueOrComponentInstance, title, message, "danger")
}

export async function toastInfo(vueOrComponentInstance, title, message){
    await showToast(vueOrComponentInstance, title, message, "info")
}
