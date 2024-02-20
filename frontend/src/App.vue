<template>
  <div id="app">
    <LoginView />
    <Booster />
  </div>
</template>
<script>
import LoginView from "./components/Login.vue";
import Booster from "./components/BoosterOpenning.vue";
import menu from "./components/Menu.vue";
export default {
  name: "App",
  components: {
    LoginView,
    menu
    Booster,
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