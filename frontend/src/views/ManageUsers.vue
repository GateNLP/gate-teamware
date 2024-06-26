<template>
  <div class="container">
    <div class="row my-3">
      <h1>Manage Users</h1>
    </div>
    <div class="row my-3">

      <div class="col-4">
        <b-form-input v-model="userSearch" placeholder="Search by username or email"></b-form-input>

        <br>

        <b-list-group id="users">
          <b-list-group-item href="#" v-for="user in usersPaginated" v-bind:key="user.id"
                             @click="selectUser(user.username)"
                             class="d-flex justify-content-between align-items-center"
                             v-b-tooltip.hover :title="user.email">
            {{ user.username }}
          </b-list-group-item>
        </b-list-group>

        <br>

        <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="users"
            align="center"
        ></b-pagination>

<!--        <b-button variant="primary" class="disabled">Create user</b-button>-->

      </div>

      <div class="col-8">
        <b-form href="" method="post">

          <b-form-group label="Username">
            <b-form-input name="username" type="text" v-model="form.username"/>
          </b-form-group>

          <b-form-group label="Email address">
            <b-form-input name="email" type="text" v-model="form.email"/>
          </b-form-group>

          <b-form-group label="Roles">
            <b-form-checkbox
                id="manager_checkbox"
                v-model="form.is_manager"
                name="manager_checkbox"
            >
              Manager
            </b-form-checkbox>
            <b-form-checkbox
                id="admin_checkbox"
                v-model="form.is_admin"
                name="admin_checkbox"
            >
              Admin
            </b-form-checkbox>

          </b-form-group>

          <b-form-group label="Activation status">
            <b-form-checkbox
                v-model="form.is_activated"
                name="account_activated"
            >
              Account activated
            </b-form-checkbox>

          </b-form-group>

          <b-form-group label="Change user password">
            <b-form href="" method="post">

              <b-form-group label="New Password">
                <b-form-input name="password" type="password" v-model="newPassword" placeholder="Enter new password"/>
              </b-form-group>

              <b-form-group label="Confirm Password">
                <b-form-input name="password_confirm" type="password" v-model="newPasswordConfirm"
                              placeholder="Type password again to confirm"/>
              </b-form-group>

              <b-form-row>
                <b-col>
                  <b-button variant="primary" @click="passwordChangeHandler">Change
                    Password
                  </b-button>
                </b-col>
              </b-form-row>
            </b-form>

          </b-form-group>

          <b-form-row class="mt-4">
            <b-col>
              <b-button variant="primary" @click="saveUserHandler">Save</b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" @click="passwordResetHandler">Trigger password reset</b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" @click="generateActivationHandler">Generate activation e-mail</b-button>
            </b-col>
            <b-col>
              <b-button variant="danger" @click="handleAccountDeleteButton">
                Delete user account
              </b-button>
            </b-col>
          </b-form-row>
        </b-form>

        <DeleteModal v-model="showDeleteUserModal"
                     :title="deleteAccountModalTitle"
                     @delete="deleteUserAccount"
        >
          <b-alert show variant="danger">Warning, this action is permanent! The personal details in the account will be removed and the user will no longer be able to login to the system using this account.</b-alert>

          <b-row v-if="allowUserDelete">
            <b-col>Also remove any annotations, projects and documents associated with the user:</b-col>
            <b-col cols="3">
              <b-checkbox v-model="permanentlyDeleteUserAccount"
                          name="delete-all-user-data"
              ></b-checkbox>
            </b-col>
          </b-row>

        </DeleteModal>
      </div>

    </div>
  </div>
</template>
<script>
import _ from "lodash"
import {mapState, mapActions, mapGetters} from "vuex";
import {toastError, toastSuccess} from "@/utils";
import DeleteModal from "../components/DeleteModal.vue";

export default {
  name: "ManageUsers",
  title: "Manage Users",
  components: {DeleteModal},
  data() {
    return {
      users: [],
      userSearch: '',
      currentPage: 1,
      perPage: 10,
      form: {
        id: null,
        username: null,
        is_manager: null,
        is_admin: null,
        email: null,
        is_activated: null,
      },
      newPassword: null,
      newPasswordConfirm: null,
      showDeleteUserModal: false,
      permanentlyDeleteUserAccount: false,
    }
  },
  methods: {
    ...mapActions(["getAllUsers", "adminGetUser", "adminUpdateUser", "adminUpdateUserPassword",
      "generatePasswordReset", "generateUserActivation", "adminDeleteUser", "adminDeleteUserPersonalInformation"]),
    searchUsers(users, searchString) {
      const regEx = new RegExp(searchString, "i");
      const result = _.filter(users, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
      return result
    },
    async selectUser(username) {
      this.form = await this.adminGetUser(username);
    },
    async saveUserHandler() {
      try {
        let response = await this.adminUpdateUser(this.form);
        this.form = response;
        this.users = await this.getAllUsers() // Refresh the user selection
        toastSuccess("Save user details", "User details saved.", this)

      } catch (e) {
        toastError("Could not save user details", e, this)
      }

    },
    async passwordChangeHandler(){
      try{
        if(this.newPassword !== this.newPasswordConfirm){
          throw new Error("Password does not match")
        }

        await this.adminUpdateUserPassword({
          username: this.form.username,
          password: this.newPassword
        })
        toastSuccess("Change user password", "User password changed", this)

      }catch (e) {
        toastError("Could not change user's password", e, this)
      }

    },
    async passwordResetHandler() {
      try {
        await this.generatePasswordReset(this.form.username)
        toastSuccess("Password reset", "Password reset email generated.", this)
      } catch (e) {
        toastError("Could not trigger password reset for " + this.form.username, e, this)
      }
    },
    async generateActivationHandler() {
      try {
        await this.generateUserActivation(this.form.username)
        toastSuccess("Activation generation", "Account activation email generated", this)

      } catch (e) {
        toastError("Could not save user details", e, this)
      }

    },
    async handleAccountDeleteButton(){
      if(this.form.username){
        this.showDeleteUserModal = true
        this.permanentlyDeleteUserAccount = false
      }
    },
    async deleteUserAccount(){
      try{
        if(this.permanentlyDeleteUserAccount){
          await this.adminDeleteUser(this.form.username)
        }
        else{
          await this.adminDeleteUserPersonalInformation(this.form.username)
        }
        toastSuccess("User deleted", `The user account ${this.form.username} (${this.form.email}) has been successfully deleted.`)
        this.permanentlyDeleteUserAccount = false
        this.users = await this.getAllUsers()
        this.clearUserForm()

      }catch (e){
        toastError("The user could not be deleted", e)
      }
    },
    clearUserForm(){
      this.form =  {
        id: null,
        username: null,
        is_manager: null,
        is_admin: null,
        email: null,
        is_activated: null,
      }
    }
  },
  async mounted() {
    this.users = await this.getAllUsers()
  },
  computed: {
    ...mapGetters(["allowUserDelete"]),
    usersFiltered() {
      return this.searchUsers(this.users, this.userSearch);
    },
    rows() {
      return this.usersFiltered.length
    },
    usersPaginated() {
      return this.usersFiltered.slice(
          (this.currentPage - 1) * this.perPage,
          this.currentPage * this.perPage
      )
    },
    deleteAccountModalTitle(){
      return `Permanenently delete ${this.form.username} (${this.form.email})?`
    }
  }
}
</script>

<style>
</style>
