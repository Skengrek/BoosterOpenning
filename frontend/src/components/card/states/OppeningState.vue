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
        position: absolute;
        z-index: 1;
    }

    .card-face {
        background-image: var(--image);
        background-size: contain;
        width: 100%; height: 100%; pointer-events: none;
        -webkit-tap-highlight-color: transparent;
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        }
    .new-icon{
        right:1%;
        top:0%;
        width:50px;
        position:absolute;
        opacity: 0.6;
        animation: shrinkGrowRotate 4s infinite;
    }

    @keyframes shrinkGrowRotate {
        0% {transform: scale(1) rotate(0deg);}
        50% {transform: scale(0.5) rotate(90deg);}
        100% {transform: scale(1) rotate(0);}
    }
</style>

<template @mousemove="mouseMove">
    <div ref="el" class="perspective-container" :style="cssProps">
        <div class="card_element" @mousedown="mouseDown" @mouseup="mouseUp">
            <img class="card-face">
            <img class="new-icon" :src="newIcon" style=""/>
            <!-- <img v-if="holo_type == 'H'" class="holo"> -->
        </div>
    </div>
</template>


<script>
import { AppStore } from '@/stores/app'
export default {
        data() {
            return {
                app: AppStore(),
                newIcon: require('@/assets/images/icons/new.svg'),
                card: null,
                el: null,
                selectedImage: this.large_image,
                width: 490,
                height: 684,
                selectedCard: null,
                isDragged: false,
                filter: null,
                cursorPosOrigin: {x: 0,y: 0},
                translation: {x: 0,y: 0},
                offsetTranslation: {x: 0,y: 0},
                offsetRotation: {x: 0,y: 0},
                rotate: {x: 0,y: 0},
                maxDep: 40,
                maxAngle: 20,
            }
        },
        mounted() {
            this.el = this.$refs.el
            this.card = this.app.cards.openCards[this.cardKey]
            this.selectedImage = this.card.large_image            
            this.el.style.top = `calc(50% - ${this.height/2}px)`
            this.el.style.left = `calc(50% - ${this.width/2}px)`

        },
        updated() {
            
        },
        computed: {
            cssProps () {
                return {
                    "--width": (this.width) + "px",
                    "--height": (this.height) + "px",
                    "--xAxis": -this.rotate.x + "deg",
                    "--yAxis": this.rotate.y + "deg",
                    "--image": `url(http://localhost:8001${this.selectedImage})`,
                    "--filter": this.filter,
                }
            }
        },
        methods: {
            fadeAway () {
                this.el.style.transition = `all 0.2s ease-out`
                this.el.style.opacity = `0`
            },
            mouseDown(e) {
                if (this.app.selected_el == null) {
                    this.app.selected_el = this
                    this.cursorPosOrigin = {
                        x: e.pageX,
                        y: e.pageY
                    }
                    const rect = this.$refs.el.getClientRects()[0]
                    this.offsetRotation = {
                        x: rect.x - e.pageX,
                        y: rect.y - e.pageY
                    }
                }
            },
            mouseMove(e) {
                const rect = this.el.getClientRects()[0]
                this.el.style.setProperty("--space", e.pageY - rect.y)
                this.el.style.setProperty("--HoloShiftW", (e.pageX - rect.x) / rect.width)
                this.el.style.setProperty("--HoloShiftH", (e.pageY - rect.y) / rect.height)
                // Set transition parameters
                this.el.style.transition = `all 0.2s ease-out`

                this.translation = {
                    x: this.cursorPosOrigin.x - e.pageX + this.offsetTranslation.x,
                    y: this.cursorPosOrigin.y - e.pageY + this.offsetTranslation.y
                }
                // Move the cards around
                const movment = {
                    x: this.translation.x,
                    y: this.translation.y, 
                }
                this.el.style.transform = `translate(${-movment.x}px, ${-movment.y}px)`
                // Calculate angle of card rotation

                const dist = {
                    x: rect.x - e.pageX - this.offsetRotation.x,
                    y: rect.y - e.pageY - this.offsetRotation.y
                } 
                
                this.rotate.x = 0
                if (Math.abs(dist.x) > this.maxDep) {
                    if (dist.x > 0) {
                        this.rotate.x = this.maxAngle
                    } else {
                        this.rotate.x = -this.maxAngle
                    }
                } else if (Math.abs(dist.x) < this.maxDep) {
                    this.rotate.x = (dist.x/this.maxDep)*this.maxAngle
                }

                this.rotate.y = 0
                if (Math.abs(dist.y) > this.maxDep) {
                    if (dist.y > 0) {
                        this.rotate.y = this.maxAngle
                    } else {
                        this.rotate.y = -this.maxAngle
                    }
                } else if (Math.abs(dist.y) < this.maxDep) {
                    this.rotate.y = (dist.y/this.maxDep)*this.maxAngle
                }
            },
            mouseUp() {
                if (this.app.selected_el === this) {
                    this.app.selected_el = null
                    this.rotate = {x: 0, y: 0}
                    this.offsetTranslation = this.translation
                    this.fadeAway()
                    setTimeout(this.app.cards.switchCardOpenToPresentation(this.cardKey), 200);
                }
            },
        },
    }
</script>
