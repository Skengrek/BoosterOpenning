<script setup>
    import { defineProps } from 'vue';
    defineProps({
        cardKey: Number
    })
</script>

<style scoped>

    .card_element {
        margin: 5px;
        width: var(--width);
        height: var(--height);
        overflow: hidden;
        border-left: -1px;
        border-radius: 10px;
        transform-style: preserve-3d;
        transform: rotateY(var(--xAxis, 0)) rotateX(var(--yAxis, 0));
        filter: var(--filter);
    }
    
    .perspective-container {
        transition: all 0.2s ease-out;
        perspective: 500px;
        z-index: 0;
    }

    .card-face {
        background-image: var(--image);
        background-size: contain;
        width: 100%; height: 100%;
    }
</style>


<template @mousemove="mouseMove">
    <div ref="el" class="perspective-container" :style="cssProps">
        <div class="card_element">
            <v-img :src="selectedImage"></v-img>
        </div>
    </div>
</template>

<script>
import { AppStore } from '@/stores/app'
export default {
        data() {
            return {
                app: AppStore(),
                card: null,
                el: null,
                selectedImage: null,
                width: 242,
                height: 340,
                selectedCard: null,
                filter: null,
            }
        },
        mounted() {
            this.card = this.app.presentationCards[this.cardKey]
            this.selectedImage = `${this.app.api.baseUrl}${this.card.large_image}`
            if (this.card.has_it != true){this.filter = "grayscale(1)"}
        },
        updated() {
            
        },
        computed: {
            cssProps () {
                return {
                    "--width": (this.width) + "px",
                    "--height": (this.height) + "px",
                    "--filter": this.filter,
                }
            }
        },
        methods: {
        },
    }
</script>
