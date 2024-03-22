import { defineStore } from 'pinia'
import { API } from '@/stores/api'

export const BoosterStore = defineStore('BoosterStore', {
    state: () => {
        return {
            api: API(),
            selected_el: null,
            boostersList: [],
        }
    },
    actions: {
        async getUserBooster() {
            this.boostersList = []
            const boosters = await this.api.listBoosters()
            for (const index in boosters["boosters"]) {
                this.boostersList.push(boosters["boosters"][index])
            }
        },
    }
})