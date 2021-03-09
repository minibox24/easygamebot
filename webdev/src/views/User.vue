<template>
  <div id="user">
    <table id="user-table">
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
        <tr class="userbox" v-for="(user, index) in users" :key="index">
          <td class="user">
            <b-avatar class="mr-1" :src="user.avatar" size="16px"/>
            <span>{{ user.name.length > 16 ? `${user.name.slice(0, 15)}...` : user.name }}</span>
            <span class="discord-tag">#{{ user.tag }}</span>
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
      users: [
        { avatar: '', name: 'Minibsdfgsdfgsdfgdox', tag: '3332', money: '123', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: '붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸', tag: '3332', money: '12344', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mindfgibox', tag: '3332', money: '124443', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mini', tag: '3332', money: '1423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mdfginibox', tag: '3332', money: '1243', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mbox', tag: '3332', money: '14444423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Minibsdfgsdfgsdfgdox', tag: '3332', money: '123', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: '붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸', tag: '3332', money: '12344', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mindfgibox', tag: '3332', money: '124443', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mini', tag: '3332', money: '1423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mdfginibox', tag: '3332', money: '1243', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mbox', tag: '3332', money: '14444423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Minibsdfgsdfgsdfgdox', tag: '3332', money: '123', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: '붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸', tag: '3332', money: '12344', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mindfgibox', tag: '3332', money: '124443', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mini', tag: '3332', money: '1423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mdfginibox', tag: '3332', money: '1243', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mbox', tag: '3332', money: '14444423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Minibsdfgsdfgsdfgdox', tag: '3332', money: '123', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: '붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸붸', tag: '3332', money: '12344', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mindfgibox', tag: '3332', money: '124443', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mini', tag: '3332', money: '1423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mdfginibox', tag: '3332', money: '1243', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' },
        { avatar: '', name: 'Mbox', tag: '3332', money: '14444423', joinAt: '2020. 03. 05', checkAt: '2020. 03. 07' }
      ],
      unit: '원',
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
}

#user-table {
  border-collapse: separate;
  border-spacing: 0 1rem;
}

.userbox {
  background: #1D2936;
  box-shadow: 2px 2px 2px 2px black;
  border-radius: 15px;
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
  width: auto;
  padding-right: 1rem;
  overflow: hidden;
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
  /*display: flex;*/
  justify-content: center;
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
