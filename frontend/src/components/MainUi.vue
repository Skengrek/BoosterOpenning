<script setup>
    import PresentationState from "./card/states/PresentationState.vue"
    import OppeningState from "./card/states/OppeningState.vue"
    import Menu from "./Menu.vue"
    import Logging from "./Login.vue"
</script>

<template>
    <Logging/>
    <Menu/>
    <div class="booster-opening">
        <div class="card-area" :key="app.boosters.boostersList">
            <div class="perspective-container" v-for=" booster in app.boosters.boostersList" :key="booster.name">
                <div class="booster" :id="booster.booster_id" @click="openBooster" @mousemove="mouseMove"
                    @mouseleave="mouseLeave" @mouseenter="mouseEnter">
                    <img class="booster-logo" :src="'http://localhost:8001/media/' + booster.logo">
                    <img class="booster-symbol" :src="'http://localhost:8001/media/' + booster.symbol">
                    <a class="booster-number">{{ booster.number }}</a>
                </div>
            </div>
        </div>
    </div>
    <div @mousemove="mouseMove">
        <div>
            <div>
                <OppeningState v-for="(card, cardKeyOpen) in app.cards.openCards" v-bind:key="card" :cardKey="cardKeyOpen"></OppeningState>
            </div>
            <div class="collection-area">
                <PresentationState v-for="(card, cardKeyPresentation) in app.cards.presentationCards" v-bind:key="card" :cardKey="cardKeyPresentation"></PresentationState>
            </div>
        </div>
    </div>
</template>

<style>
@import '../assets/styles/base.css';

.footer{
    position: bottom;
    margin: none;
}

.collection-area{
    display: flex;
    flex-wrap: wrap;
}

</style>

<script>
import { AppStore } from '@/stores/app'
export default {
        data() {
            return {
                app: AppStore(),
                state: "cards",
            }
        },
        async mounted(){
                document.body.addEventListener("mousedown", null)
                document.body.addEventListener("mouseup", null)
        },
        methods: {
            mouseMove(e) {
                if (this.app.selected_el != null){
                    if (this.app.selected_el.mouseMove != undefined) {
                        this.app.selected_el.mouseMove(e)
                    }
                }
            },
            mouseUp(){
                if (this.app.selected_el != null){
                    if (this.app.selected_el.mouseUp != undefined) {
                        this.app.selected_el.mouseUp()
                    }
                }
            },
            async openBooster() {
                await this.app.cards.openBooster()
            }
        },

    }
</script>
