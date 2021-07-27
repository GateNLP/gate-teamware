<template>
    <div class="container">
        <h3>My Account</h3>
        <div class="container">
            <div class="row mt-3">
                <b>Username:</b> {{user.username}}
            </div>

            <div class="row mt-3">
                <b>User Role:</b> {{user.user_role}}
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

        <b-row class="row mt-3" v-if="!isActivated">
          <b-col>
            <p class="alert-warning p-2">
              Your account must be activated before you can use the website. If you have not received the
              activation e-mail, you can re-generate it using the button below.
            </p>
            <div>
              <b-button variant="primary" @click="generateActivationCodeBtnHandler">
                  Re-send verification e-mail.
              </b-button>

            </div>

            <p v-if="activationEmailSent" class="alert-success p-4 mb-4 mt-3">
              The activation token has been re-sent to the e-mail address you used to
              register your account.
            </p>

            <p v-if="activationEmailError" class="alert-warning p-4 mb-4 mt-3">
              {{activationEmailError}}
            </p>
          </b-col>

        </b-row>

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
import {mapState, mapActions, mapGetters} from "vuex";
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
                user_role: "annotator",
                created: null,
                email: null,
            },
            form:{
                email: null,
                password: null,
                confirmpassword: null,
            },
            activationEmailSent: false,
            activationEmailError: null,
            annotation_documents: [],
        }
    },
    computed: {
      ...mapGetters(["isActivated"]),
    },
    methods: {
    ...mapActions(["getUser","changeEmail","changePassword","getUserAnnotations", "generateUserActivation"]),
        async EmailSubmitHandler(){
            await this.changeEmail(this.form);
            this.user = await this.getUser();
        },
        async FormHandler(){
            if (this.error){
                return
            }
            await this.changePassword(this.form);
        },
        async generateActivationCodeBtnHandler(){
            try{
              await this.generateUserActivation(this.user.username)
              this.activationEmailSent = true
              this.activationEmailError = null
            }catch(e){
              this.activationEmailSent = false
              this.activationEmailError = e.message
            }

        }
    },
    async mounted(){
        this.user = await this.getUser();
        this.annotation_documents = await this.getUserAnnotations();
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
