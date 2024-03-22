<script setup>
    import { defineProps } from 'vue';
    defineProps({
        card: Object,
        state: {
            type: String,
            default: "collection"
        },
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
        position: var(--position);
        z-index: 0;
        opacity: var(--opacity);
        transform: translate(var(--translationX), var(--translationY))`
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
        <div class="card_element" @mousedown="mouseDown" @mouseup="mouseUp">
            <img class="card-face">
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
                el: null,
                selectedImage: this.large_image,
                position: "absolute",
                opacity: 1,
                currentState: null,
                width: 245,
                height: 342,
                zIndex: 0,
                filter: null,
                cursorPosOrigin: {
                    x: 0,
                    y: 0
                },
                translation: {
                    x: 0,
                    y: 0
                },
                offsetTranslation: {
                    x: 0,
                    y: 0
                },
                offsetRotation: {
                    x: 0,
                    y: 0
                },
                rotate: {
                    x: 0,
                    y: 0
                },
                maxDep: 40,
                maxAngle: 20,
            }
        },
        mounted() {
            this.currentState = this.state
            this.selectedImage = this.card.large_image
            if (this.card.has_it != true){this.filter = "grayscale(1)"}
        },
        updated() {
            if (this.currentState == "collection"){
                this.zIndex = 0
                this.position = "absolute"
                this.translation= {x: 0, y: 0}
            }
            else if (this.currentState == "open"){
                this.zIndex = 1
                this.position = "absolute"
                this.opacity = 1
            }
        },
        computed: {
            cssProps () {
                return {
                    "--width": this.width + "px",
                    "--height": this.height + "px",
                    "--xAxis": -this.rotate.x + "deg",
                    "--yAxis": this.rotate.y + "deg",
                    "--image": `url(http://localhost:8001${this.selectedImage})`,
                    "--filter": this.filter,
                    "--position": this.position,
                    "--opacity": this.opacity,
                    "--translationX": this.translation.x,
                    "--translationY": this.translation.y,
                }
            }
        },
        methods: {
            mouseDown(e) {
                console.log(this.currentState)
                if (this.currentState === "open"){this.mouseDownOpen(e)}
            },
            mouseMove(e) {
                if (this.currentState === "open"){this.mouseMoveOpen(e)}
            },
            mouseUp() {
                if (this.currentState === "open"){this.mouseUpOpen()}
            },
            openToCollection() {
                this.opacity = 1
                this.currentState = "collection"
            },
            mouseDownOpen(e) {
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
            mouseMoveOpen(e) {
                const el = this.$refs.el
                const rect = el.getClientRects()[0]
                el.style.setProperty("--space", e.pageY - rect.y)
                el.style.setProperty("--HoloShiftW", (e.pageX - rect.x) / rect.width)
                el.style.setProperty("--HoloShiftH", (e.pageY - rect.y) / rect.height)

                // Set transition parameters
                el.style.transition = `all 0.2s ease-out`

                this.translation = {
                    x: this.cursorPosOrigin.x - e.pageX + this.offsetTranslation.x,
                    y: this.cursorPosOrigin.y - e.pageY + this.offsetTranslation.y
                }
                // Move the cards around
                const movment = {
                    x: this.translation.x,
                    y: this.translation.y, 
                }
                el.style.transform = `translate(${-movment.x}px, ${-movment.y}px)`
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
            mouseUpOpen() {
                if (this.app.selected_el === this) {
                    this.app.selected_el = null
                    this.rotate = {x: 0, y: 0}
                    this.offsetTranslation = this.translation
                    this.openToCollection()
                }
            }
        },
    }
</script>
