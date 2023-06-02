<template>
    <div class="booster-opening">
        <div v-if="!open" class="perspective-container">
            <div class="booster" @click="openIt" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                <img class="center" :src="'http://localhost:8000' + this.booster.image">

            </div>
        </div>
        <button class="newpack-button" v-if="open" @click="getData">New Pack</button>
        <div v-if="open" class="card-area">
            <div class="perspective-container" v-for="card in cards" :key="card.id">
                <div class="card" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
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
const axios = require('axios').default
export default {
    data() {
        return {
            cards: [],
            booster: '',
            open: false,
            selectedCard: null,
            target: null,
            centerX: null,
            centerY: null,
        }
    },
    methods: {
        async getData() {
            try {
                const response = await axios.get('http://localhost:8000/api/card/booster/open');
                this.cards = response.data.cards;
                this.booster = response.data.booster;
                this.open = false
            } catch (error) {
                console.log(error);
            }
        },

        openIt() {
            this.open = !this.open;
            this.target.style.transition = `all 0.5s ease`;
            this.target.style.transform = `rotateY(0deg) rotateX(0deg)`;
        },

        mouseEnter(e) {
            this.target = e.target;
            // Get the parent element to compute the center (parent element is not affected by 3D effects)
            let targetRect = this.target.parentElement.getClientRects()[0]
            this.centerX = targetRect.x + targetRect.width / 2;
            this.centerY = targetRect.y + targetRect.height / 2;

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
            this.target.style.setProperty("--space", e.pageY - targetRect.y);

            // Holo effect
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