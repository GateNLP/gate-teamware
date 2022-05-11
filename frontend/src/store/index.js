import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie'
import JSRPCClient from '../jrpc'

const rpc = new JSRPCClient("/rpc/")

Vue.use(Vuex)


export default new Vuex.Store({
    state: {
        user: {
            username: "",
            isAuthenticated: false,
            isManager: false,
            isAdmin: false,
            isActivated: false,
        },
    },
    getters:{
        isAuthenticated: state => state.user.isAuthenticated,
        isManager: state => state.user.isManager,
        isAdmin: state => state.user.isAdmin,
        isActivated: state => state.user.isActivated,
        username: state => state.user.username,
    },
    mutations: {
        activateUser(state){
          state.user.isActivated = true
        },
        updateUser(state, params) {
            state.user.username = params.username;
            state.user.isAuthenticated = params.isAuthenticated;
            state.user.isManager = params.isManager;
            state.user.isAdmin = params.isAdmin;
            state.user.isActivated = params.isActivated;
        },
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
                dispatch("updateUser",response)
                return response
            }catch (e){
                console.error(e)
                throw e
            }
        },
        async logout({dispatch, commit}) {
            let params = {
                username: "",
                isAuthenticated: false,
                isActivated: false,
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
                console.error(e)
                throw e
            }
        },
        async generateUserActivation({dispatch, commit}, username){
            try{
                let response = await rpc.call("generate_user_activation", username)

            }catch (e){
                console.error(e)
                throw e
            }
        },
        async activateAccount({dispatch, commit}, {username, token}){
            try{
                let response = await rpc.call("activate_account", username, token)
                await dispatch("is_authenticated")

            }catch (e){
                console.error(e)
                throw e
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
                console.error(e)
                throw e
            }
        },
        async generatePasswordReset({dispatch, commit}, username){
            try{

                let response = await rpc.call("generate_password_reset", username)

            }catch(e){
                console.error(e)
                throw e
            }

        },
        async resetPassword({dispatch, commit}, {username, token, newPassword}){
            try{

                let response = await rpc.call("reset_password", username, token, newPassword)

            }catch(e){
                console.error(e)
                throw e
            }

        },
        async setUserReceiveMailNotification({dispatch, commit}, do_receive_notification){
            try{
                let response = await rpc.call("set_user_receive_mail_notifications", do_receive_notification)
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async is_authenticated({dispatch, commit}) {
            try{
                let response = await rpc.call("is_authenticated");
                dispatch("updateUser",response);
                return response
            }catch (e){
                console.error(e)
                throw e
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

        async adminGetUser({dispatch, commit}, username) {
            try{
                let user = await rpc.call("get_user", username);
                return user
            }catch (e){
                console.error(e);
            }
        },

        async adminUpdateUser({dispatch, commit}, params) {
            try{
                const payload = {
                    id: params.id,
                    username: params.username,
                    email: params.email,
                    is_manager: params.is_manager,
                    is_admin: params.is_admin,
                    is_activated: params.is_activated,
                }
                let user = await rpc.call("admin_update_user",payload);
                return user
            }catch (e){
                console.error(e)
                throw e
            }
        },
        async adminUpdateUserPassword({dispatch, commit}, {username, password}){
            try{
                await rpc.call("admin_update_user_password", username, password)
            }catch (e){
                console.error(e)
                throw e
            }
        },

        async getAllUsers({dispatch,commit}){
            try {
                let users = await rpc.call("get_all_users");
                return users
            } catch (e){
                console.log(e)
            }
        },
        async getUserAnnotatedProjects({dispatch,commit}){
            try {
                let projects = await rpc.call("get_user_annotated_projects");
                return projects
            } catch (e){
                console.log(e)
            }

        },
        async getUserAnnotationsInProject({dispatch,commit}, {project_id, current_page, page_size}){
            try {
                let annotatedDocs = await rpc.call("get_user_annotations_in_project", project_id, current_page, page_size);
                return annotatedDocs
            } catch (e){
                console.log(e)
            }
        },
        async getProject({dispatch,commit}, id){
            try {
                let project = await rpc.call("get_project", id);
                return project
            } catch (e){
                console.log(e)
                throw e
            }
        },
        async getProjects({dispatch,commit}, {current_page, page_size, filters=null}){
            try {
                let projects = await rpc.call("get_projects", current_page, page_size, filters);
                return projects
            } catch (e){
                console.log(e)
                throw e
            }
        },
        async getProjectDocuments({dispatch,commit}, {project_id, current_page, page_size, filters=null}){

            try {
                let documents = await rpc.call("get_project_documents",
                    project_id,
                    current_page,
                    page_size,
                    filters);
                return documents
            } catch (e){
                console.log(e)
                throw e
            }
        },
        async createProject({dispatch, commit}){
            try{
                console.log("Creating a project")
                let project = await rpc.call("create_project")
                return project
            }catch(e){
                console.log(e)
                throw e
            }
        },
        async deleteProject({dispatch, commit}, projectId){
            try{
                console.log("Creating a project")
                let result = await rpc.call("delete_project", projectId)
                return result
            }catch(e){
                console.log(e)
                throw e
            }
        },
        async updateProject({dispatch, commit}, payload){
            try{
                let project = await rpc.call("update_project", payload)
                return project
            }catch(e){
                console.log(e)
                throw e
            }
        },
        async cloneProject({dispatch, commit}, id){
            try{
                let project = await rpc.call("clone_project", id)
                return project
            }catch(e){
                console.log(e)
                throw e
            }

        },
        async importProjectConfiguration({dispatch, commit}, {id, config_dict}){
            try{
                let project = await rpc.call("import_project_config", id, config_dict)
                return project

            }catch(e){
                console.log(e)
                throw e
            }

        },
        async exportProjectConfiguration({dispatch, commit}, id){
            try{
                let project_config_dict = await rpc.call("export_project_config", id)
                return project_config_dict
            }catch(e){
                console.log(e)
                throw e
            }

        },
        async addProjectDocument({dispatch, commit}, { projectId, document}){
            try{
                let docId = await rpc.call("add_project_document", projectId, document)
            }catch (e){
                console.error(e)
                throw e
            }
        },
        async addAnnotation({dispatch, commit}, {docId, annotation}){
            try {
                let annotateId = await rpc.call("add_document_annotation", docId, annotation)
            }catch (e){
                console.error(e)
                throw e
            }
        },
        async getAnnotations({dispatch, commit}, projectID){
            try{
                let response = await rpc.call("get_annotations", projectID)
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async deleteDocumentsAndAnnotations({dispatch, commit}, {documentIds, annotationIds}){
            try{
                let response = await rpc.call("delete_documents_and_annotations", documentIds, annotationIds)
                return response

            }catch (e){
                console.error(e)
                throw e
            }

        },
        async getPossibleAnnotators({dispatch, commit}){
            try{
                let response = await rpc.call("get_possible_annotators");
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async getProjectAnnotators({dispatch, commit}, projectID){
            try{
                let response = await rpc.call("get_project_annotators", projectID);
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async addProjectAnnotator({dispatch, commit}, {projectID, username}){
            try{
                let response = await rpc.call("add_project_annotator", projectID, username);
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async removeProjectAnnotator({dispatch, commit}, {projectID, username}){
            try{
                let response = await rpc.call("remove_project_annotator", projectID, username);
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },
        async getAnnotationTimings({dispatch, commit}, projectID){
            try{
                let response = await rpc.call("get_annotation_timings", projectID);
                return response
            }catch(e){
                console.error(e)
                throw e
            }
        },

        async getUserAnnotationTask({dispatch, commit}) {
            try{
                let annotationTask = await rpc.call("get_annotation_task")
                return annotationTask
            }catch(e){
                console.error(e)
                throw e
            }

        },
        async completeUserAnnotationTask({dispatch, commit}, {annotationID, data, annotationTime}) {

            try{
                await rpc.call("complete_annotation_task", annotationID, data, annotationTime)
            }catch(e){
                console.error(e)
                throw e
            }


        },
        async rejectUserAnnotationTask({dispatch, commit}, annotationID) {
            try{
                await rpc.call("reject_annotation_task", annotationID)
            }catch(e){
                console.error(e)
                throw e
            }

        },
        async getDocumentContent({dispatch, commit}, id) {
            try{
                return await rpc.call("get_document_content", id)
            }catch(e){
                console.error(e)
                throw e
            }

        },
        async getAnnotationContent({dispatch, commit}, id) {
            try{
                return await rpc.call("get_annotation_content", id)
            }catch(e){
                console.error(e)
                throw e
            }

        },
        async getEndpointListing({dispatch, commit}){
            try{
                return await rpc.call("get_endpoint_listing")
            }catch(e){
                console.error(e)
                throw e
            }
        }


    },
    modules: {}
})
