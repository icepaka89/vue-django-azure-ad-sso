<template>
    <div>
        <div style="padding: 15px;">
            <h1>Login</h1>
            <input v-model="username" placeholder="username" />
            <br />
            <input v-model="password" type="password" placeholder="password"/>
            <br/>
            <button @click="login()" style="padding: 10px 40px">Log In</button>
            <p v-if="errorMessage.length > 0" style="color: red; font-weight: bold">
                {{errorMessage}}
            </p>
        </div>
        or
        <div style="padding: 15px">
            <a href="http://localhost:8000/api/sso_signin">
                <img src="../assets/ms-symbollockup_signin_light.png" />
            </a> 
        </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
            errorMessage: ""
        }
    },
    methods: {
        login() {
            axios.defaults.withCredentials = true;
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.post(
                '/api/signin', 
                { username: this.username, password: this.password }
            ).then(() => {
                this.$router.push('/');
            }).catch((err) => {
                this.errorMessage = "Invalid username and password";
                console.error(err);
            });
        }
    }
}
</script>
<style scoped>
input {
    margin: 5px;
}
button:hover {
    cursor: pointer;
}
</style>