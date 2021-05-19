import Vue from 'vue'
import AnnotationApp from './AnnotationApp.vue'
import router from './router'
import store from './store'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import {mapActions} from 'vuex'


// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

//Importing scss assets needs an @/ in front of it
import "@/assets/sass/app.scss"

Vue.use(BootstrapVue)
// Vue.use(IconsPlugin) //optional

Vue.config.productionTip = false

new Vue({
  router,
  store,
  methods: {
    ...mapActions(["updateUser"]),
},
  mounted() {
    //Adds user's details reactive
    if (store.user) {
        this.updateUser(store.user);
    }
  },
  render: h => h(AnnotationApp)
}).$mount('#app')
