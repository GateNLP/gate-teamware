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

const toastDelay = 5000  //ms of delay
const toastFailedDelay = 15000  //ms of delay
let defaultVueOrComponentInstance = null

/**
 * Set a a vue or component instance as a root for displaying toasts
 * @param vueOrComponentInstance
 */
export function initToast(vueOrComponentInstance){
    defaultVueOrComponentInstance = vueOrComponentInstance
}

/**
 * Shows a notification
 * @param title Title message
 * @param message Message body
 * @param variant The colour variant of the toast
 * @param delay ms delay until notification is hidden
 * @param noAutoHide Toast will not hide automatically if set to true
 * @param vueOrComponentInstance The component that's used to display the toast, if null then the
 * component provided in initToast will be used instead
 * @returns {Promise<void>}
 */
export async function showToast(title, message, variant, delay = 2000, noAutoHide = false, vueOrComponentInstance=null){
    let toastRoot = defaultVueOrComponentInstance
    if(vueOrComponentInstance)
        toastRoot = defaultVueOrComponentInstance
    toastRoot.$bvToast.toast(message, {
        title: title,
        toaster: 'b-toaster-top-right',
        variant: variant,
        autoHideDelay: delay,
        noAutoHide: noAutoHide,
        })
}

/**
 * Shows a success notification
 * @param title Title message
 * @param message Message body
 * @param vueOrComponentInstance The component that's used to display the toast, if null then the
 * component provided in initToast will be used instead
 * @returns {Promise<void>}
 */
export async function toastSuccess(title, message, vueOrComponentInstance = null){
    await showToast(title, message, "success", toastDelay, false, vueOrComponentInstance)
}

/**
 * Shows a failed notification
 * @param title Title message
 * @param errorObj Error object as body
 * @param vueOrComponentInstance The component that's used to display the toast, if null then the
 * component provided in initToast will be used instead
 * @returns {Promise<void>}
 */
export async function toastError(title, errorObj, vueOrComponentInstance = null){
    if(errorObj.code === JSRPCClient.AUTHENTICATION_ERROR){
        // Diverts to login page if it's an authentication error
        vueOrComponentInstance.$router.push("/login")
    }else{
        await showToast(title, errorObj.message, "danger", toastFailedDelay, true, vueOrComponentInstance)
    }
}

/**
 * Shows an information notification
 * @param title Title message
 * @param message Message body
 * @param vueOrComponentInstance The component that's used to display the toast, if null then the
 * component provided in initToast will be used instead
 * @returns {Promise<void>}
 */
export async function toastInfo(title, message, vueOrComponentInstance = null){
    await showToast(title, message, "info", toastDelay, false, vueOrComponentInstance)
}
