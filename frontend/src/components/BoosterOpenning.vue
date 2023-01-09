<template>
    <div class="booster_container">
        <div class="booster_content">
            <h1 v-html="this.booster.name"></h1>
            <img v-if="!open" class="center" @click="openIt" :src="'http://localhost:8000'+this.booster.image">
            <button class="newpack" v-if="open" @click="getData">New Pack</button>
            <ul v-if="open" class="cards_list horizontal-list">
                <li v-for="card in cards" :key="card.id">
                    <div>
                        <div class="">
                            <p class="card__shine basic v pokémon"><img 
                            :src="'http://localhost:8000'+card.small_image"></p>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<style lang="scss">
    @import '../assets/styles/card.css';
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
            selectedCard: null;
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
        },

        onmousemove(event) {
            var el = document.querySelector(".card");

            var x = event.clientX
            var y = event.clientY

            var HEIGHT = document.body.clientHeight;
            var WIDTH = document.body.clientWidth;

            var calcY = Math.round(map_range(x, 0, WIDTH, -33, 33));
            var calcX = Math.round(map_range(y, 0, HEIGHT, 33, -33));

            Velocity.hook(el, "rotateX", calcX / 3 + "deg");
            Velocity.hook(el, "rotateY", calcY / 3+ "deg");

        }
    },
    created() {
        this.getData();
    }
}
</script>