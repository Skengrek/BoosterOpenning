// stores/counter.js
import { defineStore } from 'pinia'

export const loginStore = defineStore('loginStore', {
    state: () => {
        return {
            isLogged: false,
            access: 0,
            refresh: 0,
        }
    },
    actions: {
        updateTokens(access, refresh) {
            this.access = access
            this.refresh = refresh
            this.isLogged = true
        },
        getAccessToken() {
            return this.access
        },
        getRefreshToken() {
            return this.refresh
        },
        isUserLogged() {
            return this.isLogged
        }
    },
})