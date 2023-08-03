import { defineStore } from 'pinia'
const axios = require('axios').default

export const API = defineStore('API', {
    state: () => {
        return {
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
            try {
                let response = await axios({
                    method: 'post',
                    url: 'http://localhost:8000/api/token/',
                    data: { username: username, password: password },
                    headers: { "content-type": "application/json" }
                })
                this.access = response.data.access
                this.refresh = response.data.refresh
                this.isLogged = true
                return true
            } catch (error) {
                this.isLogged = false
                console.log(error)
                return false
            }
        },
        /**
         * Call the Api to create a user
         * @param {string} username 
         * @param {string} password 
         * @param {string} email 
         * @returns 
         */
        async register(username, password, email) {
            try {
                axios.defaults.xsrfHeaderName = 'x-csrftoken'
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.withCredentials = true
                let response = await axios({
                    method: 'post',
                    url: 'http://localhost:8000/api/users/',
                    data: {
                        username: username,
                        password: password,
                        email: email
                    },
                    headers: { "content-type": "application/json" }
                })
                if (response.status === 201) {
                    return this.login(username, password)
                } else {
                    return false
                }

            } catch (error) {
                console.log(error)
                return false
            }
        },
        /**
         * List all booster the user logged has access
         */
        async listBooster() {
            if (this.isLogged != true) {
                throw 'Cannot list booster, User is not logged'
            }
            try {
                axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
                let response = await axios({
                    method: 'GET',
                    url: 'http://localhost:8000/api/cards/booster/user/list',
                    headers: {
                        "content-type": "application/json",
                        "Authorization": `Bearer ${this.access}`,
                        'Access-Control-Allow-Origin': "*",
                        'Access-Control-Allow-Methods': "GET, LIST",
                    }
                })
                if (response.status === 201) {
                    return response.data
                } else {
                    return false
                }
            } catch (error) {
                throw new TypeError(error, "store-api")
            }
        }
    },
})