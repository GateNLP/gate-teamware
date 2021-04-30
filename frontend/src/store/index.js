import Vue from 'vue'
import Vuex from 'vuex'
import JSRPCClient from '../jrpc'

const rpc = new JSRPCClient("/rpc/")

Vue.use(Vuex)


export default new Vuex.Store({
    state: {
        projects: null,
    },
    mutations: {
        updateProjects(state,projects) {
            state.projects = projects;
        }
    },
    actions: {
        async login({dispatch, commit}, username, password) {

        },
        async logout({dispatch, commit}) {

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
