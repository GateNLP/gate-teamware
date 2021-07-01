import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie'
import JSRPCClient from '../jrpc'

const rpc = new JSRPCClient("/rpc/")

Vue.use(Vuex)


export default new Vuex.Store({
    state: {
        projects: null,
        user: {
            username: "",
            isAuthenticated: false,
        },
    },
    mutations: {
        updateUser(state, params) {
            state.user.username = params.username;
            state.user.isAuthenticated = params.isAuthenticated;
        },
        updateProjects(state,projects) {
            state.projects = projects;
        }
    },
    actions: {
        updateUser({commit}, params) {
            commit("updateUser", params);
        },
        async login({dispatch, commit}, params) {
            try{
                const payload = {
                    username: params.username,
                    password: params.password,
                }
                let response = await rpc.call("login",payload);
                dispatch("updateUser",response);
                return response
            }catch (e){
                console.error(e);
            }
        },
        async logout({dispatch, commit}) {
            let params = {
                username: "",
                isAuthenticated: false,
            }
            await rpc.call("logout");
            commit("updateUser", params);
        },
        async register({dispatch, commit}, params) {
            try{
                const payload = {
                    username: params.username,
                    password: params.password,
                    email: params.email,
                }
                let response = await rpc.call("register",payload);
                dispatch("updateUser",response);
                return response
            }catch (e){
                console.error(e);
            }
        },
        async changeEmail({dispatch, commit}, params) {
            try{
                const payload = {
                    email: params.email,
                }
                await rpc.call("change_email",payload);
            }catch (e){
                console.error(e);
            }
        },
        async changePassword({dispatch, commit}, params) {
            try{
                const payload = {
                    password: params.password,
                }
                let response = await rpc.call("change_password",payload);
                return
            }catch (e){
                console.error(e);
            }
        },

        async is_authenticated({dispatch, commit}) {
            try{
                let response = await rpc.call("is_authenticated");
                dispatch("updateUser",response);
                return response
            }catch (e){
                console.error(e);
            }
        },

        async getUser({dispatch, commit}) {
            try{
                let user = await rpc.call("get_user_details");
                return user
            }catch (e){
                console.error(e);
            }
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
        async addProjectDocument({dispatch, commit}, { projectId, document}){
            try{
                let docId = await rpc.call("add_project_document", projectId, document)
            }catch (e){
                console.error(e)
            }
        },
        async addAnnotation({dispatch, commit}, {docId, annotation}){
            try {
                let annotateId = await rpc.call("add_document_annotation", docId, annotation)
            }catch (e){
                console.log(e)
            }
        },
        async getAnnotations({dispatch, commit}, projectID){
            try{
                let response = await rpc.call("get_annotations", projectID)
                return response
            }catch(e){
                console.log(e)
            }
        },
        async getPossibleAnnotators({dispatch, commit}){
            try{
                let response = await rpc.call("get_possible_annotators");
                return response
            }catch(e){
                console.log(e)
            }
        },
        async getProjectAnnotators({dispatch, commit}, projectID){
            try{
                let response = await rpc.call("get_project_annotators", projectID);
                return response
            }catch(e){
                console.log(e)
            }
        },
        async addProjectAnnotator({dispatch, commit}, {projectID, username}){
            try{
                let response = await rpc.call("add_project_annotator", projectID, username);
                return response
            }catch(e){
                console.log(e)
            }
        },
        async removeProjectAnnotator({dispatch, commit}, {projectID, username}){
            try{
                let response = await rpc.call("remove_project_annotator", projectID, username);
                return response
            }catch(e){
                console.log(e)
            }
        },

        async getUserAnnotationTask({dispatch, commit}) {
            let annotationTask = await rpc.call("get_annotation_task")
            return annotationTask
        },
        async completeUserAnnotationTask({dispatch, commit}, {annotationID, data}) {
            await rpc.call("complete_annotation_task", annotationID, data)

        },
        async rejectUserAnnotationTask({dispatch, commit}, annotationID) {
            await rpc.call("reject_annotation_task", annotationID)
        },
        async getDocumentContent({dispatch, commit}, id) {
            return await rpc.call("get_document_content", id)
        },
        async getAnnotationContent({dispatch, commit}, id) {
            return await rpc.call("get_annotation_content", id)
        },


    },
    modules: {}
})
