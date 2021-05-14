import Vue from 'vue'
import AnnotationApp from './AnnotationApp.vue'
import router from './router'
import store from './store'
import { BootstrapVue, BootstrapVueIcons, IconsPlugin } from 'bootstrap-vue'



// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

//Importing scss assets needs an @/ in front of it
import "@/assets/sass/app.scss"

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
// Vue.use(IconsPlugin) //optional

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(AnnotationApp)
}).$mount('#app')
