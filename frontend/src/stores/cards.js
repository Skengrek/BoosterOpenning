import { defineStore } from 'pinia'
import { API } from '@/stores/api'

export const CardStore = defineStore('CardStore', {
    state: () => {
        return {
            api: API(),
            boosters: {},
            nb_booster_available: 0,
        }
    },
    actions: {
        async loadUserData() {
            let user_booster = await this.api.listBoosters()
            let nb_booster_available = 0
            for (const key in user_booster["boosters"]) {
                let value = user_booster["boosters"][key]
                this.boosters[value.booster_id] = value
                nb_booster_available += value.number
            }
            this.nb_booster_available = nb_booster_available
        },
    }
})