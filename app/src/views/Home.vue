<template>
  <div class="home">
    <h1>Welcome home {{$store.getters.username}}!</h1>

    <button v-if="$store.getters.isLoggedIn" @click="signout">
      Sign out
    </button>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
// import AzureADLoginBtn from '@/components/AzureADLoginBtn'

export default {
  name: 'Home',
  components: {
    // HelloWorld,
    // AzureADLoginBtn
  },
  mounted() {
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.get("/api/currentuser")
    .then((resp) => {
      console.log(resp);
      this.$store.commit('setUser', resp.data);
      this.$store.commit('setIsLoggedIn', true)
    })
    .catch((err) => {
      console.log(err);
      this.$router.push('/login')
    });
  },
  methods: {
    signout() {
      document.cookie = '';
      localStorage.clear();
      this.$store.commit('setUser', '');
      this.$store.commit('setIsLoggedIn', false);

      axios.get('/api/signout').then(() => {
        window.location = "/";
      });
    }
  }
}
</script>
