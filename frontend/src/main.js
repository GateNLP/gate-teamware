import 'vite/modulepreload-polyfill'
import Vue from 'vue'
import AnnotationApp from './AnnotationApp.vue'
import router from './router'
import store from './store'
import titleMixin from "@/utils/titleMixin";




import {mapActions} from 'vuex'
import {BootstrapVue, BootstrapVueIcons, IconsPlugin} from 'bootstrap-vue'
import VJsoneditor from 'v-jsoneditor'
import MarkdownItVue from 'markdown-it-vue'


//Importing scss assets needs an @/ in front of it

import "@/assets/sass/app.scss"

// Import Bootstrap an BootstrapVue CSS files (after app.scss, which includes bootstrap)
import 'bootstrap-vue/dist/bootstrap-vue.css'



Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VJsoneditor)
Vue.use(MarkdownItVue)
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
    await store.dispatch("initialise")

    new Vue({
        router,
        store,
        render: h => h(AnnotationApp)
    }).$mount('#app')

}
initialiseApp()



