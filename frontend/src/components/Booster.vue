<template>
    <div class="booster-opening">
        <div v-if="userStore.view_booster_list">
            <div class="card-area" :key="userStore.boosters">
                <div class="perspective-container" v-for=" booster in userStore.boosters_to_show" :key="booster.name">
                    <div class="booster" :id="booster.booster_id" @click="openBooster" @mousemove="mouseMove"
                        @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                        <img class="booster-logo" :src="'http://localhost:8001/media/' + booster.logo">
                        <img class="booster-symbol" :src="'http://localhost:8001/media/' + booster.symbol">
                        <a class="booster-number">{{ booster.number }}</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    // const axios = require('axios').default
    import { API } from '@/stores/api'
    import { UserStore } from '@/stores/user'
    export default {
        data() {
            return {
                api: API(),
                userStore: UserStore(),
                number_of_card: [],
                number_of_owned_card: [],
                cards: [],
                show_booster_list: false,
                show_cards: false,
                show_open_collection: false,
                selectedCard: null,
                target: null,
                centerX: null,
                centerY: null,
            }
        },
        methods: {}
    }
</script>