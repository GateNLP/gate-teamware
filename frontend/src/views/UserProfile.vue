<template>
    <div class="container">
        <h3>My Account</h3>
        <div class="container">
            <div class="row mt-3">
                <b>Username:</b> {{user.username}}
            </div>

            <div class="row mt-3">
                <b>Email: </b> {{user.email}}
                <b-icon icon="pencil-square" @click="editEmail = !editEmail" variant="primary"></b-icon>
            </div>

            <div class="row mt-3" v-if="editEmail">
            <b-form href="" method="post">
        
            <b-form-group label="Change Email">
                <b-form-input type="text" v-model="form.email"/>

                <b-button variant="primary" @click="EmailSubmitHandler" :class="{'disabled': error!=''}">Submit</b-button>
            </b-form-group>
            </b-form>
            </div>

            <div class="row mt-3">
                <b>Joined: </b> {{user.created | datetime}}
            </div>

        <div class="row mt-3">
            <b-form href="" method="post">
                
                <b-form-group label="New Password">
                    <b-form-input type="password" v-model="form.password" placeholder="Enter new password"/>
                </b-form-group>

                <b-form-group label="Confirm Password">
                    <b-form-input type="password" v-model="form.confirmpassword" placeholder="Type password again to confirm"/>
                </b-form-group>

                <div class="alert alert-warning" role="alert" v-if="error">
                    {{ error }}
                </div>

                <b-form-row>
                    <b-col>
                        <b-button variant="primary" @click="FormHandler" :class="{'disabled': error!=''}">Change Password</b-button>
                    </b-col>
                </b-form-row>
            </b-form>
        </div>
        </div>

        <div class="row my-3">
            <h3>My Annotations</h3>
        </div>
        <div v-if="annotation_documents">
            <DocumentsList :documents="annotation_documents"></DocumentsList>
        </div>
        <div v-else>
            No annotations yet
        </div>
    </div>
</template> 
<script>
import {mapState, mapActions} from "vuex";
import DocumentsList from "@/components/DocumentsList";

export default {
    name: "UserProfile",
    components: {DocumentsList},
    data(){
        return{
            error: "",
            editEmail: false,
            user: {
                username: null,
                created: null,
                email: null,
            },
            form:{
                email: null,
                password: null,
                confirmpassword: null,
            },
            annotation_documents: [],
        }
    },
    methods: {
    ...mapActions(["getUser","changeEmail","changePassword","getUserAnnotations"]),
        async EmailSubmitHandler(){
            await this.changeEmail(this.form);
            this.user = await this.getUser();
        },
        async FormHandler(){
            if (this.error){
                return
            }
            await this.changePassword(this.form);
        }
    },
    async mounted(){
        this.user = await this.getUser();
        this.annotation_documents = await this.getUserAnnotations();
        console.log(typeof(annotation_documents))
    },
    watch: {
        form: {
            immediate: true,
            deep: true,
            handler(form) {
                if (form.confirmpassword != form.password){
                    this.error = 'Password must match';
                } else {
                    this.error = '';
                }
            }
        }
    }
}
</script>

<style>
</style>
