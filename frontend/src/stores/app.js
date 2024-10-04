import { defineStore } from 'pinia'
import { API } from './api'

export const AppStore = defineStore('AppStore', {
    state: () => {
        return {
            api: API(),
            backCard: [],
            openCards: [],
            openCardsLoaded: 0,
            presentationCards: [],
            boosters: [],
            selected_el: null,
            presentationMode: false
        }
    },
    actions: {
        async login(username, password){
            const logged = await this.api.login(username, password)
            if (logged){
                this.loadUserData()
            }
            return logged
        },
        async register(username, password, mail){
            return await this.api.register(username, password, mail)
        },
        async openBooster(boosterKey){
            const boosterExt = this.boosters[boosterKey].booster_id
            const newCards = await this.api.openBooster(boosterExt)
            this.openCards = []
            this.openCardsLoaded = 0
            this.presentationCards = []
            for (const index in newCards["cards"].reverse()) {
                this.openCards.push(newCards["cards"][index])
            }
        },
        async loadUserData() {
            this.boosters = []
            const boosters = await this.api.listBoosters()
            for (const index in boosters["boosters"]) {
                this.boosters.push(boosters["boosters"][index])
            }
        },
        async getUserCollection() {
            const newCards = await this.api.listCards()
            this.openCards = []
            this.presentationCards = []
            this.boosters = []
            for (const index in newCards["cards"]) {
                this.presentationCards.push(newCards["cards"][index])
            }
            this.presentationMode = true
        },
        switchToOpenning(){
            this.openCards = []
            this.presentationCards = []
            this.boosters = []
            this.presentationMode = false
            this.loadUserData()
        },
        switchCardOpenToPresentation(cardId) {
            let card = this.openCards[cardId]
            card.has_it = true
            this.openCards.splice(cardId, 1)
            this.presentationCards.push(card)
        },
        async disconnect() {
            this.openCards = []
            this.presentationCards = []
            this.boosters = []
            this.presentationMode = false
            this.api.disconnect()
        },
    }
})