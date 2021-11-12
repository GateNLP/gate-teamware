import JSRPCClient from '../jrpc'

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

export async function showToast(vueOrComponentInstance, title, message, variant, delay = 2000){
    vueOrComponentInstance.$bvToast.toast(message, {
        title: title,
        toaster: 'b-toaster-top-right',
        variant: variant,
        autoHideDelay: delay,
        })
}

export async function toastSuccess(vueOrComponentInstance, title, message){
    await showToast(vueOrComponentInstance, title, message, "success")
}

export async function toastError(vueOrComponentInstance, title, errorObj){
    if(errorObj.code === JSRPCClient.AUTHENTICATION_ERROR){
        // Diverts to login page if it's an authentication error
        vueOrComponentInstance.$router.push("/login")
    }else{
        await showToast(vueOrComponentInstance, title, errorObj.message, "danger")
    }
}

export async function toastInfo(vueOrComponentInstance, title, message){
    await showToast(vueOrComponentInstance, title, message, "info")
}
