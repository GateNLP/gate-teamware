<template>
    <div class="container">
        <div class="row my-3">
            <h3>Manage Users</h3>
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

                <b-button variant="primary" class="disabled">Create user</b-button>

                </div>

                <div class="col-8">
                    <b-form href="" method="post">
                
                        <b-form-group label="Username">
                            <b-form-input type="text" v-model="form.username"/>
                        </b-form-group>

                        <b-form-group label="Email address">
                            <b-form-input type="text" v-model="form.email"/>
                        </b-form-group>

                        <b-form-checkbox
                        id="manager_checkbox"
                        v-model="form.is_manager"
                        name="manager_checkbox"
                        unchecked-value="not_accepted"
                        >
                        Manager
                        </b-form-checkbox>

                        <b-form-checkbox
                        id="admin_checkbox"
                        v-model="form.is_admin"
                        name="admin_checkbox"
                        unchecked-value="not_accepted"
                        >
                        Admin
                        </b-form-checkbox>

                        <b-form-row>
                            <b-col>
                                <b-button variant="primary" @click="FormHandler">Save</b-button>
                            </b-col>
                            <b-col>
                                <b-button variant="primary" class="disabled">Trigger password reset</b-button>
                            </b-col>
                        </b-form-row>
                    </b-form>
                </div>

        </div>
    </div>
</template> 
<script>
import _ from "lodash"
import {mapState, mapActions} from "vuex";

export default {
    name: "ManageUsers",
    components: {},
    data(){
        return{
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
            },
        }
    },
    methods: {
    ...mapActions(["getAllUsers", "adminGetUser","adminUpdateUser"]),
        searchUsers(users,searchString){
            const regEx = new RegExp(searchString);
            const result = _.filter(users, ({username, email}) => !!username.match(regEx) || !!email.match(regEx));
            return result
        },
        async selectUser(username){
            this.form = await this.adminGetUser(username);
        },
        async FormHandler(){
            let response = await this.adminUpdateUser(this.form);
            this.form = response;
        },
    },
    async mounted(){
        this.users = await this.getAllUsers()
    },
    computed:{
        usersFiltered(){
            return this.searchUsers(this.users,this.userSearch);
        },
        rows() {
            return this.usersFiltered.length
        },
        usersPaginated(){
            return this.usersFiltered.slice(
                (this.currentPage - 1) * this.perPage,
                this.currentPage * this.perPage
            )
        },
    }
}
</script>

<style>
</style>
