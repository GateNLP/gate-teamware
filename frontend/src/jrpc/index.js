import Cookies from 'js-cookie'
import axios from 'axios'

class JRPCClient{

    static PARSE_ERROR = -32700
    static INVALID_REQUEST = -32600
    static METHOD_NOT_FOUND = -32601
    static INVALID_PARAMS = -32602
    static INTERNAL_ERROR = -32603
    static AUTHENTICATION_ERROR = -32000
    static UNAUTHORIZED_ERROR = -32001

    #endpointUrl = null
    #csrfToken = null
    #messageCounter = 0


    constructor(endpointUrl) {
        this.#endpointUrl = endpointUrl
        this.loadCsrfFromCookie()
    }

    loadCsrfFromCookie(){

        const token = Cookies.get('csrftoken')

        if(token) {
            axios.defaults.headers.common['X-CSRFToken'] = token
        }
        else{
            console.error("Could not get CSRF token from cookie!")

        }
    }

    setCsrfToken(token){
        this.#csrfToken = token
        axios.defaults.headers.common['X-CSRFToken'] = token
    }

    /**
     * Call the RPC method `methodName` with parameters `params`.
     *
     * On failure, always throw an Error object with an error code in the .code property.
     * The code corresponds to the error codes defined in the class (based on JSON-RPC spec)
     *
     * @param methodName
     * @param params
     * @returns {Promise<*>}
     */
    async call(methodName, ...params){
        this.loadCsrfFromCookie()
        try{
            this.#messageCounter += 1
            const response = await axios.post(this.#endpointUrl, {
                jsonrpc: "2.0",
                method: methodName,
                params: params,
                id: this.#messageCounter
            })

            const message = response.data
            return message.result
        }catch (e){
            if(e?.response?.data?.error?.code && e?.response?.data?.error?.message){
                // If the returned error is fully formed json-rpc (endpoint reached)
                const err = new Error(e?.response?.data?.error?.message)
                err.code = e?.response?.data?.error?.code
                throw err
            }
            else{
                // Not a fully formed json-rpc response, may be a problem with the endpoint
                // or connection to the server
                // TODO: Do we care about specific connection errors?
                const err = new Error("Unknown error")
                err.code = JRPCClient.INTERNAL_ERROR
                throw err
            }
        }
    }
}

export default JRPCClient
