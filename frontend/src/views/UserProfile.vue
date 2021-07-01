<template>
    <div class="container">
        <div class="container">
            <div class="row mt-3">
                <b>Username: </b>{{user.username}}
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
    </div>
</template> 
<script>
import {mapState, mapActions} from "vuex";

export default {
    name: "UserProfile",
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
            }
        }
    },
    methods: {
    ...mapActions(["getUser","changeEmail","changePassword"]),
        async EmailSubmitHandler(){
            await this.changeEmail(this.form);
            this.user = await this.getUser();
        },
        async FormHandler(){
            if (this.error){
                return
            }
            let response = await this.changePassword(this.form);
            if (response.error){
                this.error = response.error;
            }
        }
    },
    async mounted(){
        this.user = await this.getUser();
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
