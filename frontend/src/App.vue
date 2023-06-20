<template>
  <div id="app">
    <LoginView />
    <Booster />
  </div>
</template>
<script>
import Booster from "./components/BoosterOpenning.vue";
import LoginView from "./components/Login.vue";
export default {
  name: "App",
  components: {
    Booster,
    LoginView,
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>