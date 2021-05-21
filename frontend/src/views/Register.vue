<template>
    <div class="container">
        <h3>Register</h3>
        <b-form href="" method="post">
            
            <b-form-group label="Username">
                <b-form-input type="text" v-model="form.username"/>
            </b-form-group>

            <b-form-group label="Email">
                <b-form-input type="text" v-model="form.email"/>
            </b-form-group>

            <b-form-group label="Password">
                <b-form-input type="password" v-model="form.password"/>
            </b-form-group>

            <b-form-group label="Confirm Password">
                <b-form-input type="password" v-model="form.confirmpassword" placeholder="Type password again to confirm"/>
            </b-form-group>

            <div class="alert alert-warning" role="alert" v-if="error">
                {{ error }}
            </div>

            <b-form-row>
                <b-col>
                    <b-button variant="primary" @click="FormHandler" :class="{'disabled': error!=''}">Register</b-button>
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
            error: "",
            form: {
                username: null,
                password: null,
                email: null,
                confirmpassword: null,
            },
        }
    },
    methods: {
    ...mapActions(["register"]),
    async FormHandler(){
        if (this.error){
            return
        }
        let response = await this.register(this.form);
        if (!response.error){
            this.$router.push({ name: 'Home' });
        }
    }
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
