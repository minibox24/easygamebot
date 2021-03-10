<template>
  <div id="setting">
    <div class="buttons">
      <b-button class="mr-2" @click="showPW = !showPW">비밀번호 {{ showPW ? '숨기기' : '보이기' }}</b-button>
      <b-button class="mr-2" variant="primary" @click="save">저장</b-button>
      <b-button variant="danger" @click="reset">초기화</b-button>
    </div>
    <div class="boxes">
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
        <div style="display: flex; align-items: center">
          <span class="title">아이템</span>
          <b-icon
            class="ml-2" icon="plus" v-b-modal.modal-create
            variant="success" scale="2.5"
          />
        </div>
        <div class="item" v-for="(item, index) in config.game.items" v-bind:key="index">
          <span>{{ item.name }}</span>
          <div class="actions">
            <b-icon
              icon="info-circle-fill" variant="info" @click="select=item" v-b-modal.modal-info
              class="mr-1 iconbtn" v-b-tooltip.v-light.hover.top="'상세 정보'"
            />
            <b-icon
              icon="trash-fill" variant="danger" @click="itemRemove(item)"
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
    <b-modal
      id="modal-create" centered header-bg-variant="primary"
      title="아이템 생성" header-text-variant="light" @ok="itemCreate"
      cancel-title="취소" ok-title="생성" ok-variant="success"
    >
      <b-form-group
        label="아이템 이름"
        label-for="item-name"
        label-cols-sm="4"
        label-align-sm="right"
      >
        <b-form-input id="item-name" v-model="create.name"/>
      </b-form-group>
      <b-form-group
        label="아이템 설명"
        label-for="item-desc"
        label-cols-sm="4"
        label-align-sm="right"
      >
        <b-form-input id="item-desc" v-model="create.desc"/>
      </b-form-group>
      <b-form-group
        label="아이템 가격"
        label-for="item-price"
        label-cols-sm="4"
        label-align-sm="right"
      >
        <b-form-input id="item-price" type="number" v-model="create.price"/>
      </b-form-group>
      <b-form-group
        label="아이템 효과 태그"
        label-for="item-effect"
        label-cols-sm="4"
        label-align-sm="right"
      >
        <b-form-input id="item-effect" v-model="create.effect"/>
      </b-form-group>
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
      unit: this.$store.state.config.game.unit,
      create: {
        name: '',
        desc: '',
        price: 0,
        effect: ''
      }
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
    itemRemove (item) {
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
            const idx = this.config.game.items.indexOf(item)
            this.config.game.items.splice(idx, 1)
          }
        })
    },
    itemCreate () {
      this.config.game.items.push({
        name: this.create.name,
        description: this.create.desc,
        price: this.create.price,
        effect: this.create.effect
      })

      this.create = { name: '', desc: '', price: 0, effect: '' }
    }
  }
}
</script>

<style scoped>
#setting {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.buttons {
  display: flex;
  flex-direction: row;
}

.boxes {
  display: grid;
  place-items: center;
  grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
  column-gap: 2rem;
}

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

@media ( min-width: 1350px ) {
  .box {
    min-width: 20rem;
  }

  .boxes {
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  }
}
</style>
