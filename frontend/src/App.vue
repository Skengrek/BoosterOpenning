<template>
    <div id="app">
        <UI/>
    </div>
</template>
<script>
    import UI from "./components/MainUi.vue"
    export default { 
    name: "App",
    components: {
            UI,
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