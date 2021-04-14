import Vue from 'vue'
import Vuex from 'vuex'
import JSRPCClient from '../jrpc'

const rpc = new JSRPCClient("/rpc/")

Vue.use(Vuex)


export default new Vuex.Store({
  state: {
      csrfToken: null
  },
  mutations: {
    setCsrfToken(state, token){
      state.csrfToken = token
      rpc.setCsrfToken(token)
    }

  },
  actions: {
    /**
     * Load csrf token from cookie obtained from django
     * @param dispatch
     * @param commit
     */
    loadCsrfToken({state, dispatch, commit}){
      const token = Cookies.get('csrftoken')
      commit('setCsrfToken', token)
      axios.defaults.headers.common['X-CSRFToken'] = state.csrfToken;
    },
    async login({dispatch, commit}, username, password){

    },
    async logout({dispatch, commit}){

    },
    async testrpc({dispatch, commit}){
      const result = await rpc.call("add", 50, 50)
      const result2 = await rpc.call("noparam")
      console.log(result)
      console.log(result2)
      await rpc.call("doesnotexist")
    }

  },
  modules: {
  }
})
