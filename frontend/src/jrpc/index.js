import Cookies from 'js-cookie'
import axios from 'axios'

class JRPCClient{

    #endpointUrl = null
    #csrfToken = null
    #messageCounter = 0

    constructor(endpointUrl) {
        this.#endpointUrl = endpointUrl
        this.loadCsrfFromCookie()
    }

    loadCsrfFromCookie(){
        const token = Cookies.get('csrftoken')
        axios.defaults.headers.common['X-CSRFToken'] = token
    }

    setCsrfToken(token){
        this.#csrfToken = token
        axios.defaults.headers.common['X-CSRFToken'] = token
    }

    async call(methodName, ...params){
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
            //TODO: Error handling!!!
            console.log(e.response.data)
        }
    }



}

export default JRPCClient
