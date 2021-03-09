import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    title: '',
    activate: '',
    icons: {
      robot: require('@/assets/robot.svg'),
      user: require('@/assets/user.svg'),
      settings: require('@/assets/settings.svg')
    },
    status: 0,
    servers: '-',
    users: '-',
    discord: {
      avatar: '',
      name: 'Bot',
      tag: '0000'
    },
    config: {
      game: {
        name: '',
        unit: '',
        register_money: 0,
        check_money: 0,
        check_time: 0,
        work_money: '',
        stock: {
          stocks: [],
          stock_default_price: 0,
          stock_change_time: 0
        },
        items: []
      },
      bot: {
        token: '',
        prefix: '',
        status: '',
        reply_mention: false
      },
      admin_tool: {
        password: ''
      }
    }
  },
  mutations: {
    setTitle (state, title) {
      state.title = title
    },
    setActivate (state, routeName) {
      const reset = () => {
        state.icons = {
          robot: require('@/assets/robot.svg'),
          user: require('@/assets/user.svg'),
          settings: require('@/assets/settings.svg')
        }
      }

      switch (routeName) {
        case 'Bot':
          reset()
          state.activate = 'robot'
          state.icons.robot = require('@/assets/robotcheck.svg')
          break
        case 'User':
          reset()
          state.activate = 'user'
          state.icons.user = require('@/assets/usercheck.svg')
          break
        case 'Setting':
          reset()
          state.activate = 'settings'
          state.icons.settings = require('@/assets/settingscheck.svg')
          break
        default:
          state.activate = ''
          reset()
      }
    },
    setStatus (state, status) {
      switch (status) {
        case 'offline':
          state.status = 0
          break
        case 'online':
          state.status = 1
          break
        default:
          state.status = 2
      }
    },
    setServerCount (state, count) {
      state.servers = count
    },
    setUserCount (state, count) {
      state.users = count
    },
    setConfig (state, data) {
      state.config = data
    }
  },
  actions: {
  },
  modules: {
  }
})
