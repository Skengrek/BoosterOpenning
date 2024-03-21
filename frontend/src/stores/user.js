import { defineStore } from 'pinia'
import { API } from '@/stores/api'

export const UserStore = defineStore('UserStore', {
    state: () => {
        return {
            api: API(),
            boosters_to_show: [],
            cards_to_show: [],
            nb_booster_available: 0,
            view_booster_list: false,
            view_pack_openning: false,
            view_collection: false,
            login: false,
            register: false,
        }
    },
    actions: {
        async login(username, password){
            return await this.api.login(username, password)
        },
        async register(username, password, mail){
            return await this.api.register(username, password, mail)
        },
        async loadUserData() {
            let user_booster = await this.api.listBoosters()
            let nb_booster_available = 0
            this.boosters_to_show = []
            for (const key in user_booster["boosters"]) {
                let value = user_booster["boosters"][key]
                this.boosters_to_show.push(value)
                nb_booster_available += value.number
            }
            this.nb_booster_available = nb_booster_available
        },

        showBoosterView(){

            this.loadUserData()
            this.main_panel_state="boosters"
            this.view_booster_list = true
            console.log(this.boosters_to_show)
        },
        async showCollectionView(){
            let data = await this.api.listCards()
            this.cards_to_show = data["cards"]
            await this.loadUserData()
            this.main_panel_state="cards"
            this.view_pack_openning = true
        },
        async openBooster(booster_extension_id) {
            let data = await this.api.openBooster(booster_extension_id)
            this.cards_to_show = data["cards"]
            // Reload data to update interface data.
            await this.loadUserData()
            this.view_pack_openning = true
        },
        async disconnect() {
            this.api.disconnect()
        }
    }
})