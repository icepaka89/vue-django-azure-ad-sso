<template>
    <button 
        v-if="account === undefined"
        @click="signIn"
    >
        Log in with Azure
    </button>
    <button 
        v-else
        @click="signOut"
    >
        {{account.name}} - Sign Out
    </button>
</template>
<script>
import { PublicClientApplication } from "@azure/msal-browser";
import axios from 'axios'

/**
 * This component demonstrates the flow for using an FE-only integration
 * for SPA apps. 
 * @see store.js for msalConfig
 */
export default {
    name: "AzureADLoginBtn",
    data() {
        return {
            account: undefined,
            signin: "https://microsoft.com",
            /**
             * @type PublicClientApplication
             */
            $msalInstance: {}
        }
    },
    created() {
        axios.defaults.withCredentials = true;
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';

        this.$msalInstance = new PublicClientApplication(
            this.$store.state.msalConfig
        );
    },
    async mounted() {
        const accounts = this.$msalInstance.getAllAccounts();
        if(accounts.length > 0) {
            this.account = accounts[0];
            const token = await this.$msalInstance.acquireTokenSilent({ account: this.account});
            console.log(token);
        }
    },
    methods: {
        async signIn() {
            await this.$msalInstance
                .loginPopup({})
                .then(async () => {
                    const accounts = this.$msalInstance.getAllAccounts();
                    this.account = accounts[0];
                    console.log(this.account);
                })
                .catch((err => {
                    console.error(`error during signIn: ${err}`);
                }));
            const token = await this.$msalInstance.acquireTokenSilent({ account: this.account});

            const result = await axios.post(
                '/api/validate', 
                { token: token.accessToken }
            );

            console.log(result);
            
        },
        async signOut() {
            await this.$msalInstance
                .logout({})
                .then(() => {
                    this.account = undefined;
                })
                .catch((err) => {
                    console.error(`error during signOut: ${err}`);
                })
        }
    }
}
</script>