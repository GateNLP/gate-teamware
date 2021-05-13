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
                let projects = await rpc.call("get_projects");
                commit("updateProjects", projects);
            } catch (e){
                console.log(e)
            }
        },
        async getProjectDocuments({dispatch,commit},payload){
            try {
                let documents = await rpc.call("get_project_documents",payload);
                return documents
            } catch (e){
                console.log(e)
            }
        },
        async createProject({dispatch, commit}){
            try{
                console.log("Creating a project")
                let project = await rpc.call("create_project")
                dispatch("getProjects")
                return project
            }catch(e){
                console.log(e)
            }
        },
        async updateProject({dispatch, commit}, payload){
            try{
                let project = await rpc.call("update_project", payload)
                dispatch("getProjects")
                return project
            }catch(e){
                console.log(e)
            }
        },
        async addAnnotation({dispatch, commit}, {docId, annotation}){
            try {

                let annotateId = await rpc.call("add_document_annotation", docId, annotation)
            }catch (e){
                console.log(e)
            }


        }



    },
    modules: {}
})
