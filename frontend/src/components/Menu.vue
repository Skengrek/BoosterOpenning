<template>
    <div>
        <button v-if="api.isLogged" class="glass-menu" @click="switchToBoosterView">Open Booster</button>
        <button v-if="api.isLogged" class="glass-menu" @click="listCards">Collection</button>

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
        async listCards() {
            const data = await this.api.listCards()
            this.cards = data.cards
            this.number_of_card = data.number_of_card
            this.number_of_owned_card = data.number_of_owned_card
            this.show_open_collection = true
            this.switchToCardView()
        },
    },
    created() {
        this.init();
    }
}
</script>