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
    status: false,
    servers: '-',
    users: [],
    discord: {
      avatar: '',
      name: 'Bot',
      tag: '0000'
    },
    com: {
      cpu: '-',
      ram: '-',
      pid: '-'
    },
    config: {
      game: {
        name: '게임봇',
        unit: '원',
        register_money: 50000,
        check_money: 15000,
        check_time: 86400,
        work_money: '500-2500',
        stock: {
          stocks: [
            '미니전자',
            '미니택배',
            '미니건설',
            '미니증권',
            '미니식품',
            '미니생명',
            '미니화재',
            '미니카드',
            '미니물산',
            '미니항공'
          ],
          stock_default_price: 5000,
          stock_change_time: 30
        },
        items: [
          { name: '니트로 클래식', description: '일의 쿨타임이 3초가 됩니다.', price: 250000, effect: 'work-speed@3' },
          { name: '니트로', description: '일의 쿨타임이 1초가 됩니다. (니트로 클래식 효과 무시)', price: 500000, effect: 'work-speed@1' },
          { name: '커피', description: '일을 해서 버는 돈이 2배가 됩니다.', price: 500000, effect: 'work-power@2' },
          { name: '몬스터', description: '일을 해서 버는 돈이 5배가 됩니다. (커피 효과 무시)', price: 500000, effect: 'work-power@5' },
          { name: '텔레파시', description: '일반 도박의 확률이 10% 증가합니다.', price: 1000000, effect: 'gamble@10' },
          { name: '밑장빼기', description: '(1회용) 일반 도박이 무조건 성공합니다.', price: 5000000, effect: '!gamble@100' },
          { name: '롤렉스', description: '사치용 아이템', price: 100000000 }
        ]
      },
      bot: {
        token: '',
        prefix: '!',
        status: '!도움',
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
      state.status = status
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
