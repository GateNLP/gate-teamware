import Vue from 'vue'
import AnnotationApp from './AnnotationApp.vue'
import router from './router'
import store from './store'

//Importing scss assets needs an @/ in front of it
import "@/assets/sass/app.scss"

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(AnnotationApp)
}).$mount('#app')
