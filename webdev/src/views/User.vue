<template>
  <div id="user">
    <div v-if="$store.state.users.length === 0" class="nothing">
      <div>
        <img src="https://discord.com/assets/263a7f4eeb6f69e46d969fa479188592.svg">
        <span>아무도 없네요.</span>
      </div>
    </div>
    <table v-else id="user-table">
      <thead>
        <tr>
          <th>유저</th>
          <th>잔액</th>
          <th>가입일</th>
          <th>출석체크일</th>
          <th>액션</th>
        </tr>
      </thead>
      <tbody>
        <tr class="userbox" v-for="(user, index) in $store.state.users" :key="index">
          <td>
            <div class="user">
              <b-avatar class="mr-1" :src="user.avatar" size="32px"/>
              <span class="discord-name">{{ user.name }}</span>
              <span class="discord-tag">#{{ user.tag }}</span>
            </div>
          </td>
          <td>{{ user.money }}{{ unit }}</td>
          <td>{{ user.joinAt }}</td>
          <td>{{ user.checkAt }}</td>
          <td>
            <b-icon
              icon="info-circle-fill" variant="info" @click="select=user" v-b-modal.modal-info
              class="mr-1 iconbtn" v-b-tooltip.v-light.hover.top="'상세 정보'"
            />
            <b-icon
              icon="trash-fill" variant="danger" @click="removeModal(user)"
              class="iconbtn" v-b-tooltip.v-light.hover.top="'삭제'"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <b-modal
      id="modal-info" centered header-bg-variant="info"
      ok-only title="상세 정보" header-text-variant="light"
    >
      <div class="profile">
        <b-avatar class="mr-2" :src="select.avatar" size="64"/>
        <span>{{ select.name }}</span>
        <span class="discord-tag">#{{ select.tag }}</span>
      </div>
      <div class="box-column">
        <div class="box-info">
          <span class="info-name">잔액</span>
          <span>{{ select.money }}{{ unit }}</span>
        </div>
        <div class="box-info">
          <span class="info-name">가입일</span>
          <span>{{ select.joinAt }}</span>
        </div>
        <div class="box-info">
          <span class="info-name">출석체크일</span>
          <span>{{ select.checkAt }}</span>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  data () {
    return {
      unit: this.$store.state.config.game.unit,
      select: {}
    }
  },
  mounted () {
    this.$store.commit('setTitle', '유저')
    this.$store.commit('setActivate', this.$route.name)
  },
  methods: {
    removeModal (user) {
      const h = this.$createElement
      const msg1 = h('p', `정말로 유저 ${user.name}#${user.tag}를 삭제할까요?`)
      const msg2 = h('b', '삭제 후 복구는 불가능합니다!!')
      this.$bvModal.msgBoxConfirm([msg1, msg2], {
        title: '유저 삭제',
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
#user {
  display: flex;
  justify-content: center;
  height: 100%;
}

.nothing {
  display: flex;
  align-items: center;
}

#user-table {
  border-collapse: separate;
  border-spacing: 0 1rem;
}

.userbox {
  background: #1D2936;
  border-radius: 15px;
  height: 3rem;
}

tr td:first-child {
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

tr td:last-child {
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

#user-table th {
  padding: .5rem;
}

#user-table td {
  width: 100px;
  padding: .5rem;
}

#user-table td:nth-child(1) {
  padding-right: 1rem;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  justify-content: left;
  align-items: center;
}

#user-table td:nth-child(2) {
  min-width: 150px;
  width: auto;
}

#user-table td:last-child {
  width: 70px;
}

#user-table td:nth-child(n+2):nth-child(-n+4),
#user-table th:nth-child(n+2):nth-child(-n+4) {
  display: none;
}

.user {
  display: flex;
  align-items: center;
}

.iconbtn {
  cursor: pointer;
}

#modal-info .profile {
  justify-content: center;
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

.profile {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.discord-name {
  display: inline-block;
  width: 150px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  vertical-align: bottom;
}

.discord-tag {
  color: gray;
}

@media ( min-width: 900px ) {
  #user-table td:nth-child(n+2):nth-child(-n+4),
  #user-table th:nth-child(n+2):nth-child(-n+4) {
    display: table-cell
  }
}
</style>
