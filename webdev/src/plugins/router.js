import Vue from 'vue'
import VueRouter from 'vue-router'
import NotFound from '../views/NotFound.vue'
import Test from '../views/Test.vue'
import Bot from '../views/Bot.vue'
import User from '../views/User.vue'
import Setting from '../views/Setting.vue'
import Login from '../views/Login'

Vue.use(VueRouter)

const requireLogin = (to, _, next) => {
  if (localStorage.getItem('password') === '1234') next()
  else {
    next({ name: 'Login', params: { path: to.path } })
  }
}

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '*',
    name: '404 Not Found',
    component: NotFound
  },
  {
    path: '/test',
    name: 'Test',
    component: Test
  },
  {
    path: '/',
    name: 'Bot',
    component: Bot,
    beforeEnter: requireLogin
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    beforeEnter: requireLogin
  },
  {
    path: '/setting',
    name: 'Setting',
    component: Setting,
    beforeEnter: requireLogin
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
