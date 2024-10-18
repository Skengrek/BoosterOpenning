<style scoped>
    .card_element {
        margin: 5px;
        width: 490px;
        height: 684px;
        overflow: hidden;
        border-left: -1px;
        border-radius: 30px;
        transform-style: preserve-3d;
        transform: rotateY(var(--xAxis, 0)) rotateX(var(--yAxis, 0));
    }
    @media screen and (max-width: 490px) {
        .card_element {
            margin: 5px;
            width: 245px;
            height: 342px;
            overflow: hidden;
            border-left: -1px;
            border-radius: 15px;
            transform-style: preserve-3d;
            transform: rotateY(var(--xAxis, 0)) rotateX(var(--yAxis, 0));
        }
    }
    
    .perspective-container {
        perspective: 500px;
        width: 100%;
        position: absolute;
        z-index: 4;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .card-face {
        background-size: contain;
        width: 100%; height: 100%; pointer-events: none;
        }
</style>

<template @mousemove="mouseMove">
    <div 
        ref="el" 
        class="perspective-container" :style="cssProps"
    >
        <div class="card_element" @mousedown="mouseDown" @mouseup="mouseUp" v-show="app.openCardsLoaded >= app.openCards.length">
            <img class="card-face" :src="image" @load="loaded">
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
                image: require('@/assets/images/back.png'),
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
                show: true,
            }
        },
        computed: {
            cssProps () {
                return {
                    "--width": (this.width) + "px",
                    "--height": (this.height) + "px",
                    "--xAxis": -this.rotate.x + "deg",
                    "--yAxis": this.rotate.y + "deg",
                    "--image": `url(${this.app.api.baseUrl}${this.selectedImage})`,
                    "--filter": this.filter,
                }
            }
        },
        methods: {
            loaded(){
                this.app.openCardsLoaded += 1
            },
            fadeAway () {
                this.$refs.el.style.transition = `all 0.2s ease-out`
                this.$refs.el.style.opacity = `0`
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
                const rect = this.$refs.el.getClientRects()[0]
                this.$refs.el.style.setProperty("--space", e.pageY - rect.y)
                this.$refs.el.style.setProperty("--HoloShiftW", (e.pageX - rect.x) / rect.width)
                this.$refs.el.style.setProperty("--HoloShiftH", (e.pageY - rect.y) / rect.height)
                // Set transition parameters
                this.$refs.el.style.transition = `all 0.2s ease-out`

                this.translation = {
                    x: this.cursorPosOrigin.x - e.pageX + this.offsetTranslation.x,
                    y: this.cursorPosOrigin.y - e.pageY + this.offsetTranslation.y
                }
                // Move the cards around
                const movment = {
                    x: this.translation.x,
                    y: this.translation.y, 
                }
                this.$refs.el.style.transform = `translate(${-movment.x}px, ${-movment.y}px)`
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
                this.$refs.el.style.transition = 'none;'
                if (this.app.selected_el === this) {
                    this.app.selected_el = null
                    this.rotate = {x: 0, y: 0}
                    this.offsetTranslation = this.translation
                    setTimeout(this.$refs.el.style.height = 0, 200);
                    setTimeout(this.$refs.el.style.width = 0, 200);
                    this.show = false
                }
            },
        },
    }
</script>
