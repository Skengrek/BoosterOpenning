<script setup>
    import PresentationState from "./card/states/PresentationState.vue"
    import OppeningState from "./card/states/OppeningState.vue"
    import Booster from "./Booster.vue"
    import Menu from "./Menu.vue"
    import Logging from "./Login.vue"
</script>

<template>
    <Logging/>
    <Menu/>
    <div class="booster-opening">
        <Booster v-for="(booster, boosterKey) in app.boosters" v-bind:key="booster" :boosterKey="boosterKey"></Booster>
    </div>
    <div @mousemove="mouseMove">
        <div>
            <div>
                <OppeningState v-for="(card, cardKeyOpen) in app.openCards" v-bind:key="card" :cardKey="cardKeyOpen"></OppeningState>
            </div>
            <div class="collection-area">
                <PresentationState v-for="(card, cardKeyPresentation) in app.presentationCards" v-bind:key="card" :cardKey="cardKeyPresentation"></PresentationState>
            </div>
        </div>
    </div>
</template>

<style>
@import '../assets/styles/base.css';

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
        },

    }
</script>
