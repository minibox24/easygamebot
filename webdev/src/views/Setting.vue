<template>
  <div id="setting">
    <div>
      <b-button class="mr-2" @click="showPW = !showPW">비밀번호 {{ showPW ? '숨기기' : '보이기' }}</b-button>
      <b-button class="mr-2" variant="primary" @click="save">저장</b-button>
      <b-button variant="danger" @click="reset">초기화</b-button>
    </div>
    <div>
      <div class="box">
        <span class="title">게임</span>
        <Input name="봇 이름" type="str" v-model="config.game.name"/>
        <Input name="돈 단위" type="str" v-model="config.game.unit"/>
        <Input name="가입 지급 돈" type="int" v-model="config.game.register_money"/>
        <Input name="출석체크 지급 돈" type="int" v-model="config.game.check_money"/>
        <Input name="출석체크 쿨타임 (초)" type="int" v-model="config.game.check_time"/>
        <Input name="일 지급 돈" type="work_money" v-model="config.game.work_money"/>
      </div>
      <div class="box">
        <span class="title">주식</span>
        <Input name="주식 종목" type="stocks" v-model="config.game.stock.stocks"/>
        <Input name="주식 초기 가격" type="int" v-model="config.game.stock.stock_default_price"/>
        <Input name="주가 변동 시간 (초)" type="int" v-model="config.game.stock.stock_change_time"/>
      </div>
      <div class="box items">
        <span class="title">아이템</span>
        <div class="item" v-for="(item, index) in config.game.items" v-bind:key="index">
          <span>{{ item.name }}</span>
          <div class="actions">
            <b-icon
              icon="info-circle-fill" variant="info" @click="select=item" v-b-modal.modal-info
              class="mr-1 iconbtn" v-b-tooltip.v-light.hover.top="'상세 정보'"
            />
            <b-icon
              icon="trash-fill" variant="danger" @click="removeModal(item)"
              class="iconbtn" v-b-tooltip.v-light.hover.top="'삭제'"
            />
          </div>
        </div>
      </div>
      <div class="box">
        <span class="title">봇</span>
        <Input name="토큰" type="password" :showpw="showPW" v-model="config.bot.token"/>
        <Input name="접두사" type="str" v-model="config.bot.prefix"/>
        <Input name="봇 상태 메시지" type="str" v-model="config.bot.status"/>
        <Input name="답장시 멘션 여부" type="bool" v-model="config.bot.reply_mention"/>
      </div>
      <div class="box">
        <span class="title">관리자 페이지</span>
        <Input name="비밀번호" type="password" :showpw="showPW" v-model="config.admin_tool.password"/>
      </div>
    </div>

    <b-modal
      id="modal-info" centered header-bg-variant="info"
      ok-only title="상세 정보" header-text-variant="light"
    >
      <div class="info">
        <h1>{{ select.name }}</h1>
        <span>{{ select.description }}</span>
      </div>
      <div class="box-column">
        <div class="box-info">
          <span class="info-name">가격</span>
          <span>{{ select.price }}{{ unit }}</span>
        </div>
        <div class="box-info">
          <span class="info-name">효과 태그</span>
          <span>{{ select.effect }}</span>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
import Input from '@/components/Input'
import axios from 'axios'

export default {
  data () {
    return {
      config: JSON.parse(JSON.stringify(this.$store.state.config)),
      showPW: false,
      select: {},
      unit: this.$store.state.config.game.unit
    }
  },
  mounted () {
    this.$store.commit('setTitle', '설정')
    this.$store.commit('setActivate', this.$route.name)
  },
  components: {
    Input
  },
  methods: {
    save () {
      this.$store.commit('setConfig', this.config)
      this.$bvToast.toast('설정을 저장했습니다!', {
        title: '완료',
        variant: 'success'
      })
    },
    reset () {
      const h = this.$createElement
      const msg1 = h('p', '정말로 설정을 초기화할까요? (토큰 제외)')
      const msg2 = h('b', '초기화 후 복구는 불가능합니다!!')
      this.$bvModal.msgBoxConfirm([msg1, msg2], {
        title: '설정 초기화',
        headerBgVariant: 'danger',
        headerTextVariant: 'light',
        okVariant: 'danger',
        okTitle: '초기화',
        cancelTitle: '취소',
        hideHeaderClose: false,
        centered: true
      })
        .then(async (value) => {
          if (value) {
            const data = (await axios.get('https://raw.githubusercontent.com/minibox24/easygamebot/master/config.json')).data
            data.bot.token = this.config.bot.token
            delete data.bot.extensions
            delete data.admin_tool.host
            delete data.admin_tool.port
            delete data.database
            this.config = data
            this.save()
          }
        })
    },
    removeModal (item) {
      const h = this.$createElement
      const msg1 = h('p', `정말로 아이템 ${item.name}을(를) 삭제할까요?`)
      const msg2 = h('b', '삭제 후 복구는 불가능합니다!!')
      this.$bvModal.msgBoxConfirm([msg1, msg2], {
        title: '아이템 삭제',
        headerBgVariant: 'danger',
        headerTextVariant: 'light',
        okVariant: 'danger',
        okTitle: '삭제',
        cancelTitle: '취소',
        hideHeaderClose: false,
        centered: true
      })
        .then(value => {
          if (value) {
            alert('삭제 처리')
          }
        })
    }
  }
}
</script>

<style scoped>
.title {
  font-weight: bold;
  font-size: 2rem;
}

.box {
  display: inline-block;
  flex-direction: column;
  border-radius: 10px;
  background: #1D2936;
  padding: 1rem;
  justify-content: center;
  margin: 1rem;
}

.items {
  width: 20rem;
}

.item {
  display: flex;
  background: #0c1c24;
  margin: .5rem;
  padding: .5rem;
  border-radius: 10px;
}

.actions {
  margin-left: auto;
}

.box-column {
  display: flex;
  justify-content: center;
}

.box-info {
  display: flex;
  flex-direction: column;
  text-align: center;
  margin: 1rem;
}

.info-name {
  font-weight: bold;
}

.info > * {
  display: flex;
  justify-content: center;
}
</style>
