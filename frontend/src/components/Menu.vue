<template>
    <div class="topnav glass-bar">
        <a v-if="api.isLogged" class="glass-button" @click="switchToBoosterView">Open Booster</a>
        <a v-if="api.isLogged" class="glass-button" @click="switchToCollection">Collection</a>
        <a v-if="api.isLogged" class="glass-button" @click="disconnect">Disconnect</a>
    </div>
</template>

<style lang="css">
    @import '../assets/styles/menu.css';
</style>

<script>
// const axios = require('axios').default
import { API } from '@/stores/api'
import { UserStore } from '@/stores/user'
export default {
    data() {
        return {
            api: API(),
            userStore: UserStore(),
        }
    },
    methods: {
        async init() {await this.userStore.loadUserData()},
        async updateData() {
        },
        async switchToBoosterView() {
            this.userStore.showBoosterView()
        },
        async switchToCollection() {
            this.userStore.showCollectionView()
        },
        async disconnect() {
            this.userStore.disconnect()
        },
    },
    created() {
        this.init();
    }
}
</script>