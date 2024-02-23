import { defineStore } from 'pinia'
import { API } from '@/stores/api'

export const CardStore = defineStore('CardStore', {
    state: () => {
        return {
            api: API(),
            boosters: {},
        }
    },
    actions: {
        async loadUserData() {
            let user_booster = await this.api.listBoosters()
            console.log(user_booster)
        },
    }
})