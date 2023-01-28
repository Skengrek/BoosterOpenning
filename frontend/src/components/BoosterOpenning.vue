<template>

    <body>
        <div class="container">
            <div class="booster" @click="openIt" @mousemove="mouseMove" @mouseleave="mouseLeave"
                @mouseenter="mouseEnter">
                <img v-if="!open" class="center" :src="'http://localhost:8000' + this.booster.image">
            </div>
        </div>
        <button class="newpack-button" v-if="open" @click="getData">New Pack</button>
        <ul v-if="open" class="cards_list horizontal-list">
            <li class="perspective" v-for="card in cards" :key="card.id">
                <div class="container">
                    <div class="card" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                        <img :src="'http://localhost:8000' + card.small_image" class="">

                    </div>
                </div>
            </li>
        </ul>


        <!-- DEBUG part of the page -->
        <div class="debug">
            <div class="glare" id="glare"></div>
            <!-- A circle to spot center of elements mainly for 3D effect debugging -->
            <span class="dot debug-red" id="debug-center-card-point"></span>
            <span class="dot debug-green" id="debug-mouse-point"></span>
        </div>

    </body>
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
                const response = await axios.get('http://localhost:8000/api/card/booster/');
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
            let targetRect = this.target.getClientRects()[0]
            this.centerX = targetRect.x + targetRect.width / 2;
            this.centerY = targetRect.y + targetRect.height / 2;

            // Change transition parameter
            this.target.style.transition = `none`;

            //Debug middle of card
            let el = document.getElementById('debug-center-card-point');
            el.style.left = `${this.centerX}px`;
            el.style.top = `${this.centerY}px`;
        },

        mouseMove(e) {
            // 3D Effect
            let xAxis = (this.centerX - e.pageX) / 8;
            let yAxis = (this.centerY - e.pageY) / 8;
            this.target.style.transform = `rotateY(${xAxis}deg) rotateX(${-yAxis}deg)`

            // Glare Effect
            this.target.style.setProperty("--x", e.pageX);
            this.target.style.setProperty("--y", e.pageY);

            // Debug point to the mouse
            let el2 = document.getElementById('glare');
            el2.style.setProperty("--x", e.pageX);
            el2.style.setProperty("--y", e.pageY);

            // Debug point to the mouse
            let el = document.getElementById('debug-mouse-point');
            el.style.setProperty("--x", e.pageX);
            el.style.setProperty("--y", e.pageY);
        },

        mouseLeave() {
            this.target.style.transition = `all 0.5s ease`;
            this.target.style.transform = `rotateY(0deg) rotateX(0deg)`
        }
    },
    created() {
        this.getData();
    }
}
</script>