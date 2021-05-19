<template>
    <div class="container">
        <h3>Register</h3>
        <b-form href="" method="post">
            
            <b-form-group label="Username">
                <b-form-input type="text" v-model="username"/>
            </b-form-group>

            <b-form-group label="Email">
                <b-form-input type="text" v-model="email"/>
            </b-form-group>

            <b-form-group label="Password">
                <b-form-input type="password" v-model="password"/>
            </b-form-group>

            <b-form-group label="Confirm Password">
                <b-form-input type="password" v-model="confirmpassword" placeholder="Type password again to confirm"/>
            </b-form-group>

            <div class="alert alert-warning" role="alert" v-if="error">
                {{ error }}
            </div>

            <b-form-row>
                <b-col>
                    <b-button variant="primary" @click="null">Register</b-button>
                </b-col>
            </b-form-row>
        </b-form>
    </div>
</template> 
<script>
import {mapState, mapActions} from "vuex";

export default {
    data(){
        return{
            error: false,
            username: null,
            password: null,
            email: null,
            confirmpassword: null,
        }
    },
    methods: {
    // ...mapActions(),
    }
}
</script>

<style>
</style>
