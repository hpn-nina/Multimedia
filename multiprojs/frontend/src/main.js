import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createStore } from 'vuex'

const app = createApp(App)

const store = createStore({
    state() {
        return {

        }
    },
    mutations: {


    },
    getters: {


    }
})

app.use(router)
app.mount('#app')
app.use(store)