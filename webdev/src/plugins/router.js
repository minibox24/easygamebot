import Vue from 'vue'
import VueRouter from 'vue-router'
import NotFound from '../views/NotFound.vue'
import Test from '../views/Test.vue'
import Bot from '../views/Bot.vue'
import User from '../views/User.vue'
import Setting from '../views/Setting.vue'

Vue.use(VueRouter)

const routes = [
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
    component: Bot
  },
  {
    path: '/user',
    name: 'User',
    component: User
  },
  {
    path: '/setting',
    name: 'Setting',
    component: Setting
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
