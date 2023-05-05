import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import store from "@/store"

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {guest: true},
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue'),
        meta: {guest: true},
    },
    {
        path: '/privacypolicy',
        name: 'Privacy Policy',
        component: () => import('@/views/PrivacyPolicy.vue'),
        meta: {guest: true},
    },
    {
        path: '/terms',
        name: 'Terms & Conditions',
        component: () => import('@/views/TermsAndConditions.vue'),
        meta: {guest: true},
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: {guest: true},
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Register.vue'),
        meta: {guest: true},
    },

    {
        path: '/activate',
        name: 'ActivateAccount',
        component: () => import('@/views/ActivateAccount.vue'),
        meta: {guest: true},
    },
    {
        path: '/passwordreset',
        name: 'PasswordReset',
        component: () => import('@/views/PasswordReset.vue'),
        meta: {guest: true},
    },
    {
        path: '/account',
        name: 'UserAccount',
        component: () => import('@/views/UserAccount.vue'),
        meta: {requiresAuth: true},
    },
    {
        path: '/user_annotations',
        name: 'UserAnnotations',
        component: () => import('@/views/UserAnnotations.vue'),
        meta: {requiresAuth: true},
    },
    {
        path: '/projects',
        name: 'Projects',
        component: () => import('@/views/Projects.vue'),
        meta: {requiresManager: true},
    },
    {
        path: '/project/:projectId',
        name: 'Project',
        component: () => import('@/views/Project.vue'),
        props: true,
        meta: {requiresManager: true},
    },
    {
        path: '/annotate',
        name: 'Annotate',
        component: () => import('@/views/Annotate.vue'),
        meta: {requiresAuth: true},
    },
    {
        path: '/manageusers',
        name: 'ManageUsers',
        component: () => import('@/views/ManageUsers.vue'),
        meta: {requiresAdmin: true},
    },
    {
        path: '/cookies',
        name: 'Cookies',
        component: () => import('@/views/Cookies.vue'),
        meta: {guest: true},
    },

]

const router = new VueRouter({
    mode: 'history',
    base: "/",
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.getters.isAuthenticated) {
            next();
            return;
        }
        next("/login");
    } else if (to.matched.some((record) => record.meta.guest)) {
        if (store.getters.isAuthenticated) {
            next();
            return;
        }
        next();
    } else if (to.matched.some((record) => record.meta.requiresManager)) {
        if (store.getters.isManager) {
            next();
            return;
        }
        next("/");
    } else if (to.matched.some((record) => record.meta.requiresAdmin)) {
        if (store.getters.isAdmin) {
            next();
            return;
        }
        next("/");
    } else {
        next();
    }
});

export default router
