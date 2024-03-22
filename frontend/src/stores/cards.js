import { defineStore } from 'pinia'
import { API } from '@/stores/api'

export const CardStore = defineStore('CardStore', {
    state: () => {
        return {
            api: API(),
            openCards: [],
            nbOfOpenCards: 0,
            presentationCards: [],
            nbOfPresentationCards: 0,
            boosters: []
        }
    },
    actions: {
        async openBooster() {},
        async getPresentation() {},
        async getRandomCardToOpenState(number) {
            /* 
             * Add random cards to the booster dictionnary 
            */
            const cards = await this.api.getCardExample(number)
            for (const index in cards["cards"]) {
                this.nbOfOpenCards++
                this.openCards.push(cards["cards"][index])
            }
        },
        switchCardOpenToPresentation(cardId) {
            let card = this.openCards[cardId]
            this.openCards.splice(cardId, 1)
            this.nbOfOpenCards--
            this.nbOfPresentationCards++
            this.presentationCards.push(card)
        }
    }
})