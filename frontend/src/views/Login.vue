<template>
    <div class="container">
        <h3>Sign In</h3>
        <b-form href="" method="post">
            
            <b-form-group label="Username">
                <b-form-input type="text" v-model="username"/>
            </b-form-group>

            <b-form-group label="Password">
                <b-form-input type="password" v-model="password"/>
            </b-form-group>

            <div class="alert alert-warning" role="alert" v-if="error">
                {{ error }}
            </div>

            <b-form-row>
                <b-col>
                    <b-button variant="primary" @click="null">Sign In</b-button>
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
        }
    },
    methods: {
    ...mapActions(["login"]),
    }
}
</script>

<style>
</style>
