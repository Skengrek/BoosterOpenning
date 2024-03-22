<template>
  <div id="app">
    <LoginView />
    <Menu />
    <Booster />
  </div>
</template>
<script>
import LoginView from "./components/Login.vue";
import Booster from "./components/BoosterOpenning.vue";
import Menu from "./components/Menu.vue";
export default {
  name: "App",
  components: {
    LoginView,
    Booster,
    Menu
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