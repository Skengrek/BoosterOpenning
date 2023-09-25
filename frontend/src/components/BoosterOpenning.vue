<template>
    <div class="booster-opening">
        <div>
            <button v-if="show_menu" class="newpack-button" @click="listBoosters">List Booster</button>
            <button v-if="show_menu" class="newpack-button" @click="listCards">List Cards</button>
        </div>
        <div v-if="show_booster_list">
            <div class="card-area">
                <div class="perspective-container" v-for="booster in boosters" :key="booster.name">
                    <div class="booster" :id="booster.booster_id" @click="openBooster" @mousemove="mouseMove"
                        @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                        <img class="booster-logo" :src="'http://localhost:8000/media/' + booster.logo">
                        <img class="booster-symbol" :src="'http://localhost:8000/media/' + booster.symbol">
                        <a class="booster-number">{{ booster.number }}</a>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="show_cards" class="card-area">
            <div v-if="show_open_collection">
                <a>{{ number_of_owned_card }} / {{ number_of_card }}</a>
            </div>
            <div class="perspective-container" v-for="card in cards" :key="card.id">
                <div class="card_3D" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                    <img :src="'http://localhost:8000' + card.small_image" class="">
                    <img v-if="card.holo_type == 'H'" class="holo">
                    <span class="glare"></span>
                </div>
            </div>
        </div>
    </div>

    <!-- DEBUG part of the page -->
    <div class="debug">
        <!-- A circle to spot center of elements mainly for 3D effect debugging -->
        <span class="dot debug-red" id="debug-center-card-point"></span>
        <span class="dot debug-green" id="debug-mouse-point"></span>
    </div>
</template>

<style lang="css">
@import '../assets/styles/base.css';
</style>


<script>
// const axios = require('axios').default
import { API } from '@/stores/api'
export default {
    data() {
        return {
            store: API(),
            number_of_card: [],
            number_of_owned_card: [],
            cards: [],
            boosters: [],
            show_menu: true,
            show_booster_list: false,
            show_cards: false,
            show_open_collection: false,
            selectedCard: null,
            target: null,
            centerX: null,
            centerY: null,
        }
    },
    methods: {
        async getData() {
            try {
                this.open = false
            } catch (error) {
                console.log(error);
            }
        },
        async listBoosters() {
            const data = await this.store.listBoosters()
            this.boosters = data.boosters
            this.show_booster_list = true
            this.show_open_booster = false
        },
        async listCards() {
            const data = await this.store.listCards()
            this.cards = data.cards
            this.number_of_card = data.number_of_card
            this.number_of_owned_card = data.number_of_owned_card
            this.show_open_collection = true
            this.switchToCardView()
        },
        async openBooster() {
            // Get the booster id that you want to open
            const data = await this.store.openBooster(this.target.id)
            this.cards = data.cards
            this.show_open_collection = false
            this.switchToCardView()
        },

        switchToCardView() {
            this.show_cards = true
            this.show_booster_list = false
            this.target.style.transition = `all 0.5s ease`;
            this.target.style.transform = `rotateY(0deg) rotateX(0deg)`;
        },

        mouseEnter(e) {
            this.target = e.target;
            // Get the parent element to compute the center (parent element is not affected by 3D effects)
            let targetRect = this.target.parentElement.getClientRects()[0]
            this.centerX = targetRect.x + targetRect.width / 2 + window.scrollX;
            this.centerY = targetRect.y + targetRect.height / 2 + window.scrollY;

            // Change transition parameter
            this.target.style.transition = `none`;

            //Debug middle of card
            let el = document.getElementById('debug-center-card-point');
            el.style.left = `${this.centerX}px`;
            el.style.top = `${this.centerY}px`;
            this.target.style.setProperty("--HoloOpacity", 50);
        },

        mouseMove(e) {
            // 3D Effect
            this.target.style.setProperty("--xAxis", (this.centerX - e.pageX) / 8);
            this.target.style.setProperty("--yAxis", (this.centerY - e.pageY) / 8);

            // Glare Effect
            let targetRect = this.target.parentElement.getBoundingClientRect()
            this.target.style.setProperty("--xGlare", e.pageX - targetRect.x);
            this.target.style.setProperty("--yGlare", e.pageY - targetRect.y);

            // Holo effect
            this.target.style.setProperty("--space", e.pageY - targetRect.y);
            this.target.style.setProperty("--HoloShiftW", (e.pageX - targetRect.x) / targetRect.width);
            this.target.style.setProperty("--HoloShiftH", (e.pageY - targetRect.y) / targetRect.height);

            // Debug point to the mouse
            let el = document.getElementById('debug-mouse-point');
            el.style.setProperty("--x", e.pageX);
            el.style.setProperty("--y", e.pageY);
        },

        mouseLeave() {
            this.target.style.transition = `all 0.5s ease`;
            this.target.style.setProperty("--xAxis", 0);
            this.target.style.setProperty("--yAxis", 0);
            this.target.style.setProperty("--xGlare", -100);
            this.target.style.setProperty("--yGlare", -100);
            this.target.style.setProperty("--HoloOpacity", 0);
        }
    },
    created() {
        this.getData();
    }
}
</script>