<template>
    <div>
        <button v-if="api.isLogged" class="newpack-button" @click="listBoosters">List Booster</button>
        <button v-if="api.isLogged" class="newpack-button" @click="listCards">List Cards</button>
        <button v-if="api.isLogged" class="newpack-button" @click="updateData">Update Data</button>

    </div>
</template>

<style lang="css">
    @import '../assets/styles/menu.css';
</style>

<script>
// const axios = require('axios').default
import { API } from '@/stores/api'
import { CardStore } from '@/stores/cards'
export default {
    data() {
        return {
            api: API(),
            cardStore: CardStore(),
        }
    },
    methods: {
        async init() {/* For now their is nothing to init */},
        async updateData() {
            await this.cardStore.loadUserData()
        },
        // async listBoosters() {
        //     const data = await this.api.listBoosters()
        //     this.boosters = data.boosters
        //     this.show_booster_list = true
        //     this.show_open_booster = false
        // },
        // async listCards() {
        //     const data = await this.api.listCards()
        //     this.cards = data.cards
        //     this.number_of_card = data.number_of_card
        //     this.number_of_owned_card = data.number_of_owned_card
        //     this.show_open_collection = true
        //     this.switchToCardView()
        // },
    },
    created() {
        this.init();
    }
}
</script>