import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);
export default new Vuex.Store({
    state: {
        msalConfig: {
            auth: {
                clientId: '',
                authority: '',
            }
        },
        user: '',
        isLoggedIn: false
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setIsLoggedIn(state, isLoggedIn) {
            state.isLoggedIn = isLoggedIn;
        }
    },
    getters: {
        username(state) {
            return state.user;
        },
        isLoggedIn(state) {
            return state.isLoggedIn;
        }
    }
});