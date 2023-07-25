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
                return true
            } catch (error) {
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
        }
    },
})