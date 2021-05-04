import Vue from 'vue'
import Vuex from 'vuex'
import JSRPCClient from '../jrpc'

const rpc = new JSRPCClient("/rpc/")

Vue.use(Vuex)


export default new Vuex.Store({
    state: {
        csrfToken: null,
        projects: null,
    },
    mutations: {
        setCsrfToken(state, token) {
            state.csrfToken = token
            rpc.setCsrfToken(token)
        },
        updateProjects(state,projects) {
            state.projects = projects;
        }

    },
    actions: {
        /**
         * Load csrf token from cookie obtained from django
         * @param dispatch
         * @param commit
         */
        loadCsrfToken({state, dispatch, commit}) {
            const token = Cookies.get('csrftoken')
            commit('setCsrfToken', token)
            axios.defaults.headers.common['X-CSRFToken'] = state.csrfToken;
        },
        testnormal({dispatch, commit}){
          return "Hello world"
        },
        async testasync({dispatch}){
            return "Hello world"
        },
        async login({dispatch, commit}, username, password) {

        },
        async logout({dispatch, commit}) {

        },
        async testrpc({dispatch, commit}) {

            try {

                const result = await rpc.call("add", 50, 50)
                const result2 = await rpc.call("noparam")
                console.log(result)
                console.log(result2)

                await rpc.call("doesnotexist")

            } catch (e) {
                console.log(e.code == rpc.INTERNAL_ERROR)
            }

        },
        async getProjects({dispatch,commit}){
            try {
                let projects = await rpc.call("getProjects");
                console.log(projects);
                commit("updateProjects", projects);
            } catch (e){
                console.log(e)
            }
        }

    },
    modules: {}
})
