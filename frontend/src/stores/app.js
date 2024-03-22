import { defineStore } from 'pinia'
import { API } from './api'
import { BoosterStore } from './boosters'
import { CardStore } from './cards'

export const AppStore = defineStore('AppStore', {
    state: () => {
        return {
            api: API(),
            boosters: BoosterStore(),
            cards: CardStore(),
            selected_el: null,
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
        async loadUserData() {
            this.boosters.getUserBooster()
        },
        async disconnect() {
            this.boosters_to_show = []
            this.cards_to_show = []
            this.nb_booster_available = 0
            this.view_booster_list = false
            this.view_pack_openning = false
            this.view_collection = false
            this.api.disconnect()
        },
    }
})