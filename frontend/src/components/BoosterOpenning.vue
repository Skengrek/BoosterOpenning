<template>

    <body>
        <div class="perspective">
            <div class="container" @click="openIt" @mousemove="mouseMove" @mouseleave="mouseLeave"
                @mouseenter="mouseEnter">
                <div class="booster">
                    <img v-if="!open" class="center" :src="'http://localhost:8000' + this.booster.image">
                </div>
            </div>
        </div>
        <button class="newpack-button" v-if="open" @click="getData">New Pack</button>
        <ul v-if="open" class="cards_list horizontal-list">
            <li class="perspective" v-for="card in cards" :key="card.id">
                <div class="container" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                    <div class="card glare">
                        <img :src="'http://localhost:8000' + card.small_image">
                    </div>
                </div>
            </li>
        </ul>
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
        mouseMove(e) {
            console.log(this.target.class);

            // 3D Effect
            let xAxis = (this.centerX - e.pageX) / 8;
            let yAxis = (this.centerY - e.pageY) / 8;
            this.target.style.transform = `rotateY(${xAxis}deg) rotateX(${-yAxis}deg)`

            // Glare Effect
            const { x, y } = this.target.getBoundingClientRect();
            this.target.style.setProperty("--x", e.clientX - x);
            this.target.style.setProperty("--y", e.clientY - y);
        },
        //animate in
        mouseEnter(e) {
            this.target = e.target;
            let targetRect = this.target.getClientRects()[0]
            this.centerX = targetRect.x + targetRect.width / 2;
            this.centerY = targetRect.y + targetRect.height / 2;
            this.target.style.transition = `none`;
        },
        //animate out
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