import { defineStore } from 'pinia'
const axios = require('axios').default

export const API = defineStore('API', {
    state: () => {
        return {
            baseUrl: 'http://skengrek.fr/collectionapi/',
            isLogged: false,
            access: 0,
            refresh: 0,
        }
    },
    actions: {
        /**
         * 
         * @returns if the user is logged
         */
        isUserLogged() {
            return this.isLogged
        },
        /**
         * With a username and a password, get the access and refresh token
         *  from the API.
         * @param {string} username 
         * @param {string} password 
         */
        async login(username, password) {
            const response = await this.callAPI(
                'post',
                `${this.baseUrl}api/token/`,
                { "content-type": "application/json" },
                { username: username, password: password },
                false // Do not try refresh 
            )
            if (response.status == 200) {
                this.access = response.data.access
                this.refresh = response.data.refresh
                this.isLogged = true
                return true
            }
            else return false
        },
        /**
         * Call the Api to create a user
         * @param {string} username 
         * @param {string} password 
         * @param {string} email 
         * @returns 
         */
        async register(username, password, email) {
            const response = await this.callAPI(
                'post',
                `${this.baseUrl}api/users/create/`,
                { "content-type": "application/json" },
                {
                    username: username,
                    password: password,
                    email: email
                },
                false,
                201
            )
            if (response.status === 201) {
                return this.login(username, password)
            }
            else return false
        },
        async disconnect() {
            this.isLogged = false
            this.access = 0
            this.refresh = 0
        },
        /** Refresh the access token if you call the API but it is expired
         * 
         */
        async refreshToken() {
            const resp = await this.callAPI(
                'POST',
                `${this.baseUrl}api/token/refresh/`,
                { "content-type": "application/json" },
                { "refresh": this.refresh },
                false
            )
            if (resp.status == 200) {
                this.access = resp.data.access
                return true
            }
            else return false
        },
        async getCardExample(number) {
            const response = await this.callAPI(
                'GET',
                `${this.baseUrl}api/cards/example/${number}`,
                {
                    "content-type": "application/json",
                    'Access-Control-Allow-Origin': "*",
                }
            )
            return response.data
        },

        /**
         * List all booster the user logged has access
         */
        async listBoosters() {
            if (this.isLogged != true) {
                throw 'Cannot list booster, User is not logged'
            }
            const response = await this.callAPI(
                'GET',
                `${this.baseUrl}api/cards/booster/user/list/boosters`,
                {
                    "content-type": "application/json",
                    "Authorization": `Bearer ${this.access}`,
                    'Access-Control-Allow-Origin': "*",
                }
            )
            return response.data
        },
        /**
         * List all booster the user logged has access
         */
        async listCards() {
            if (this.isLogged != true) {
                throw 'Cannot list cards, User is not logged'
            }
            const response = await this.callAPI(
                'GET',
                `${this.baseUrl}api/cards/booster/user/list/cards`,
                {
                    "content-type": "application/json",
                    "Authorization": `Bearer ${this.access}`,
                    'Access-Control-Allow-Origin': "*",
                }
            )
            return response.data
        },
        /**
         * Ask the API to open a booster192.168.1.148:8001
         */
        async openBooster(extension_id) {
            if (this.isLogged != true) {
                throw 'HOW CAN YOU OPEN BOOSTER WITHOUT BEING CONNECTED ??'
            }
            const response = await this.callAPI(
                'GET',
                `${this.baseUrl}api/cards/booster/user/open/${extension_id}`,
                {
                    "content-type": "application/json",
                    "Authorization": `Bearer ${this.access}`,
                    'Access-Control-Allow-Origin': "*",
                }
            )
            return response.data
        },
        /** The base method to call API. It also regenerates token if they
         * are expired
         * @param {string} method 
         * @param {string} url 
         * @param {dict} headers 
         * @param {dict} data
         * @param {bool} try_refresh if the call failed do you try refresh the token ?
         * @param {int} awaited_status
         */
        async callAPI(method, url, headers, data = {}, try_refresh = true, awaited_status=200) {
            axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
            axios.defaults.xsrfHeaderName = 'x-csrftoken'
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.withCredentials = true
            try {
                const response = await axios({
                    method: method,
                    url: url,
                    headers: headers,
                    data: data
                })
                if (response.status == awaited_status) {
                    return response
                }
            } catch (error) {
                if (try_refresh && error.response.status == 401) {
                    const refresh = this.refreshToken()
                    if (refresh) {
                        return this.callAPI(method, url, headers, data, false)
                    }
                    else {
                        this.isLogged = false
                        return error.response
                    }
                }
                else {
                    return error.response
                }
            }
        }
    },
})