import Vue from 'vue'
import AnnotationApp from './AnnotationApp.vue'
import router from './router'
import store from './store'
import titleMixin from "@/utils/titleMixin";
import {mapActions} from 'vuex'
import {BootstrapVue, BootstrapVueIcons, IconsPlugin} from 'bootstrap-vue'
import VJsoneditor from 'v-jsoneditor'


// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

//Importing scss assets needs an @/ in front of it
import "@/assets/sass/app.scss"

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VJsoneditor)
// Vue.use(IconsPlugin) //optional

Vue.mixin(titleMixin)

Vue.config.productionTip = false

Vue.filter('datetime', function (dateString) {
    let date = new Date(dateString)
    return date.toLocaleDateString() + " " + date.toLocaleTimeString()
})

async function initialiseApp() {
    //Ensure authentication status is checked before we actually start the app
    //so things that depends on user's logged in status works properly (e.g. routing)
    await store.dispatch("is_authenticated")

    new Vue({
        router,
        store,
        render: h => h(AnnotationApp)
    }).$mount('#app')

}
initialiseApp()



