<template>
  <div class="container">
    <h1>My Account</h1>
    <b-row class="mt-3">
      <b-col>
        <b>Username:</b> {{ user.username }}
      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col>
        <b>User Role:</b> {{ user.user_role }}
      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col>
        <b>Email: </b> {{ user.email }}
        <a @click.prevent="editEmail = !editEmail"><b-icon icon="pencil-square" variant="primary"></b-icon></a>

      </b-col>
    </b-row>

    <b-row class="mt-3" v-if="editEmail">
      <b-col>
        <b-form href="" method="post">

          <b-form-group label="Change Email">
            <b-form-input name="email_change" type="text" v-model="form.email"/>

            <b-button variant="primary" @click="EmailSubmitHandler" :class="{'disabled': error!=''}">Submit</b-button>
          </b-form-group>
        </b-form>

      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col>
        <b>Joined: </b> {{ user.created | datetime }}

      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col>
        <div v-if="!editPassword">
          <b>Password:</b>*****
          <a @click.prevent="editPassword = !editPassword">
            <b-icon icon="pencil-square"  variant="primary"></b-icon>
          </a>
        </div>
        <b-form href="" method="post" v-else>

          <b-form-group label="New Password">
            <b-form-input name="password" type="password" v-model="form.password" placeholder="Enter new password"/>
          </b-form-group>

          <b-form-group label="Confirm Password">
            <b-form-input name="password_confirm" type="password" v-model="form.confirmpassword"
                          placeholder="Type password again to confirm"/>
          </b-form-group>

          <div class="alert alert-warning" role="alert" v-if="error">
            {{ error }}
          </div>

          <b-form-row>
            <b-col>
              <b-button variant="primary" @click="PasswordFormHandler" :class="{'disabled': error!=''}">Change
                Password
              </b-button>
            </b-col>
          </b-form-row>
        </b-form>

      </b-col>
    </b-row>

    <b-row class="mt-3">
      <b-col>
        <b-form inline>
          <b class="mr-2">Receive email notifications:</b>
          <b-form-checkbox v-model="user.receive_mail_notifications" switch @change="userReceiveNotificationMailChangeHandler"></b-form-checkbox>

        </b-form>

      </b-col>
    </b-row>

    <AccountActivationGenerator></AccountActivationGenerator>

  </div>
</template>
<script>
import {mapState, mapActions, mapGetters} from "vuex";

import AccountActivationGenerator from "@/components/AccountActivationGenerator";
import ProjectIcon from "@/components/ProjectIcon";
import UserAnnotatedProject from "@/components/UserAnnotatedProject";

export default {
  name: "UserAccount",
  title: "My Account",
  components: {AccountActivationGenerator},
  data() {
    return {
      error: "",
      editEmail: false,
      editPassword: false,
      user: {
        username: null,
        user_role: "annotator",
        created: null,
        email: null,
        receive_mail_notifications: false,
      },
      form: {
        email: null,
        password: null,
        confirmpassword: null,
      },
      activationEmailSent: false,

    }
  },
  computed: {
    ...mapGetters(["isActivated"]),
  },
  methods: {
    ...mapActions(["getUser", "changeEmail", "changePassword",
      "setUserReceiveMailNotification", "generateUserActivation"]),
    async EmailSubmitHandler() {
      try{
        await this.changeEmail(this.form);
        this.user = await this.getUser();
        this.editEmail = false
      }catch (e){
        toastError("Could not change e-mail", e, this)
      }

    },
    async PasswordFormHandler() {
      try {
        if (this.error) {
          return
        }
        await this.changePassword(this.form)
        this.editPassword = false
      } catch (e) {
        toastError("Could not change password", e, this)
      }

    },
    async userReceiveNotificationMailChangeHandler(){
      try{
        await this.setUserReceiveMailNotification(this.user.receive_mail_notifications)
      }catch (e){
        toastError("Could not change user mail notification preference", e, this)
      }
    },
  },
  async mounted() {
    this.user = await this.getUser();
  },
  watch: {
    form: {
      immediate: true,
      deep: true,
      handler(form) {
        if (form.confirmpassword != form.password) {
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