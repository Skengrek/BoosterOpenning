<template>
    <div v-if="app.api.isLogged" class="topnav glass-bar">
        <a class="glass-button" @click="switchToBoosterView">
            Open Booster
        </a>
        <a class="glass-button" @click="switchToCollection">
            Collection
        </a>
        <a class="glass-button" @click="disconnect">
            Disconnect
        </a>
    </div>
</template>

<style lang="css">
    .glass-bar {
        position: absolute;
        top: 0px;
        right: -3px;
        display: inline-block;
        overflow: hidden;
        border: 0;
        text-decoration: none;
        border-radius: 15px;
        background-color: rgba(138, 74, 74, 0.1);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(30px);
        color: rgba(255,255,255,0.8);
        font-size: 14px;
        letter-spacing: 2px;
        cursor: pointer;
        text-transform: uppercase;
        margin:3px;
        width: 100%;
        height: 50px;
    }

    .glass-button:hover {
        background-color: rgba(255,255,255,0.2);
    }

    .topnav a {
        float: left;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
    }
</style>

<script>
// const axios = require('axios').default
import { AppStore } from '@/stores/app'
export default {
    data() {
        return {
            app: AppStore(),
        }
    },
    methods: {
        async init() {},
        async updateData() {},
        async switchToBoosterView() {},
        async switchToCollection() {},
        async disconnect() {
            this.app.disconnect()
        },
    },
    created() {
        this.init();
    }
}
</script>