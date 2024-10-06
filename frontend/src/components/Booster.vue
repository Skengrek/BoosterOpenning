<script setup>
    import { defineProps } from 'vue';
    defineProps({
        boosterKey: Number
    })
</script>

<template>
    <div class="booster" @click="openBooster" @mousemove="mouseMove"
        @mouseleave="mouseLeave" @mouseenter="mouseEnter" v-if="number>0">
        <img class="booster-logo" :src="`${app.api.baseUrl}/media/${logo}`">
        <img class="booster-symbol" :src="`${app.api.baseUrl}/media/${symbol}`">
        <a class="booster-number">{{ number }}</a>
    </div>
</template>

<script>
    // const axios = require('axios').default
    import { AppStore } from '@/stores/app'
    export default {
        data() {
            return {
                app: AppStore(),
                logo: "",
                symbol: "",
                number: "",
                extension: "",
            }
        },
        mounted() {
            const booster = this.app.boosters[this.boosterKey]
            this.logo = booster.logo
            this.symbol = booster.symbol
            this.number = booster.number
            this.extension = booster.booster_id
        },
        methods: {
            async openBooster() {
                this.number -= 1 
                await this.app.openBooster(this.boosterKey)
            },
        }
    }
</script>