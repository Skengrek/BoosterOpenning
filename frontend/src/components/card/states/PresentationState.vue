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
    }
    
    .perspective-container {
        transition: all 0.2s ease-out;
        perspective: 500px;
        z-index: 0;
    }

    .card-face {
        background-image: var(--image);
        background-size: contain;
    }

    img {width: 100%; height: 100%; pointer-events: none;
        -webkit-tap-highlight-color: transparent;
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        }
</style>


<template @mousemove="mouseMove">
    <div ref="el" class="perspective-container" :style="cssProps">
        <div class="card_element">
            <img class="card-face">
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
                selectedImage: this.large_image,
                original_width: 245,
                width: 245,
                original_height: 342,
                height: 342,
                selectedCard: null,
                filter: null,
            }
        },
        mounted() {
            this.card = this.app.cards.presentationCards[this.cardKey]
            this.selectedImage = this.card.large_image
            if (this.card.has_it != true){this.filter = "grayscale(1)"}
        },
        updated() {
            
        },
        computed: {
            cssProps () {
                return {
                    "--width": (this.width) + "px",
                    "--height": (this.height) + "px",
                    "--image": `url(http://localhost:8001${this.selectedImage})`,
                    "--filter": this.filter,
                }
            }
        },
        methods: {
        },
    }
</script>
