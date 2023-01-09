<template>
  <div id="app">
    <Booster />
  </div>
</template>
<script>
import Booster from "./components/BoosterOpenning.vue";
export default {
  name: "App",
  components: {
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