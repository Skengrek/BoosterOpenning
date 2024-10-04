<script setup>
    import PresentationState from "./card/PresentationState.vue"
    import OppeningState from "./card/OppeningState.vue"
    import Back from "./card/Back.vue"
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
                <Back v-if="app.openCards.length>0"></Back>
                <OppeningState v-for="(card, cardKeyOpen) in app.openCards" v-bind:key="card" :cardKey="cardKeyOpen"></OppeningState>
            </div>
            <v-container fluid>
                <v-row class="d-flex flex-wrap">
                    <PresentationState 
                        v-for="(presentationCard, index) in paginatedCards" 
                        :cardKey="(page - 1) * itemsPerPage + index" 
                        v-bind:key="presentationCard"/>
                </v-row>
                <v-row v-if="app.presentationMode" >
                    <v-col cols="5" class="navigation-bar">
                        <v-pagination v-model="page" :length="totalPages" @input="nextPage"></v-pagination>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </div>
</template>

<style>
@import '../assets/styles/base.css';

.collection-area{
    display: flex;
    flex-wrap: wrap;
}

.v-pagination {
    color: white;
}

</style>

<script>
import { AppStore } from '@/stores/app'
export default {
        data() {
            return {
                app: AppStore(),
                page: 1,
                state: "cards",
                itemsPerPage: 10,
            }
        },
        async mounted(){
                document.body.addEventListener("mousedown", null)
                document.body.addEventListener("mouseup", null)
        },
        computed: {
            totalPages() {
                return Math.ceil(this.app.presentationCards.length / this.itemsPerPage);
            },
            paginatedCards() {
                if (!this.app.presentationCards) return [];
                const start = (this.page - 1) * this.itemsPerPage;
                const end = start + this.itemsPerPage;
                return this.app.presentationCards.slice(start, end);
            },
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
            nextPage(page) {
                this.page = page
            },
        },

    }
</script>
