<template>
    <div v-if="userStore.view_collection" class="card-area">
        <div class="perspective-container" v-for="card in userStore.cards_to_show" :key="card.id">
            <div class="card_3D" @mousemove="mouseMove" @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                <img :src="'http://localhost:8001' + card.small_image" class="">
                <img v-if="card.holo_type == 'H'" class="holo">
                <span class="glare"></span>
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
            target: null
        }
    },
    methods: {
        async getData() {
            try {
                this.open = false
            } catch (error) {
                console.log(error)
            }
        },
        async openBooster() {
            // Get the booster id that you want to open
            await this.userStore.openBooster(this.target.id)
            this.switchToCardView()
            console.log(this.userStore.cards_to_show)
        },

        switchToCardView() {
            this.show_cards = true
            this.show_booster_list = false
            this.target.style.transition = `all 0.5s ease`
            this.target.style.transform = `rotateY(0deg) rotateX(0deg)`
            this.resizeHandler()
        },

        mouseEnter(e) {
            this.target = e.target;
            // Get the parent element to compute the center (parent element is not affected by 3D effects)
            let targetRect = this.target.parentElement.getClientRects()[0]
            this.centerX = targetRect.x + targetRect.width / 2 + window.scrollX
            this.centerY = targetRect.y + targetRect.height / 2 + window.scrollY

            // Change transition parameter
            this.target.style.transition = `none`

            //Debug middle of card
            let el = document.getElementById('debug-center-card-point')
            el.style.left = `${this.centerX}px`
            el.style.top = `${this.centerY}px`
        },

        mouseMove(e) {
            // 3D Effect
            this.target.style.setProperty("--xAxis", (this.centerX - e.pageX) / 8)
            this.target.style.setProperty("--yAxis", (this.centerY - e.pageY) / 8)

            // Glare Effect
            let targetRect = this.target.parentElement.getBoundingClientRect()
            this.target.style.setProperty("--xGlare", e.pageX - targetRect.x - window.scrollX)
            this.target.style.setProperty("--yGlare", e.pageY - targetRect.y - window.scrollY)

            // Holo effect
            this.target.style.setProperty("--space", e.pageY - targetRect.y)
            this.target.style.setProperty("--HoloShiftW", (e.pageX - targetRect.x) / targetRect.width)
            this.target.style.setProperty("--HoloShiftH", (e.pageY - targetRect.y) / targetRect.height)

            // Debug point to the mouse
            let el = document.getElementById('debug-mouse-point')
            el.style.setProperty("--x", e.pageX)
            el.style.setProperty("--y", e.pageY)
        },

        mouseLeave() {
            this.target.style.transition = `all 0.5s ease`
            this.target.style.setProperty("--xAxis", 0)
            this.target.style.setProperty("--yAxis", 0)
            this.target.style.setProperty("--xGlare", -100)
            this.target.style.setProperty("--yGlare", -100)
        }
    },
    created() {
        this.getData()
    }
}
</script>