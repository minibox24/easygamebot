<template>
  <div id="bot">
    <div class="profile">
      <b-avatar class="mr-3" :src="this.$store.state.discord.avatar" size="128px"/>
      <span class="discord-name">{{ this.$store.state.discord.name }}</span>
      <span class="discord-tag">#{{ this.$store.state.discord.tag }}</span>
      <span class="botname">({{ this.$store.state.config.game.name }})</span>
    </div>
    <div class="buttons mt-3">
      <b-button-group size="lg">
        <b-button variant="success">시작</b-button>
        <b-button variant="danger">종료</b-button>
        <b-button variant="info">재시작</b-button>
      </b-button-group>
    </div>
    <div class="boxes mt-1">
      <div class="box status-box">
        <div class="box-column">
          <div class="box-info">
            <span class="info-name">상태</span>
            <span>{{ this.$store.state.status ? '온라인' : '오프라인' }}</span>
          </div>
          <div class="box-info">
            <span class="info-name">업타임</span>
            <span>-</span>
          </div>
        </div>
        <div class="box-column">
          <div class="box-info">
            <span class="info-name">서버 수</span>
            <span>{{ this.$store.state.servers }}</span>
          </div>
          <div class="box-info">
            <span class="info-name">가입 유저 수</span>
            <span>{{ this.$store.state.users.length }}</span>
          </div>
        </div>
      </div>
      <div style="display: flex" class="flex-column">
        <div class="box token-box">
          <div>
            <span class="info-name">봇 토큰</span>
            <b-button @click="showtoken = !showtoken">{{ showtoken ? '숨기기' : '보이기' }}</b-button>
          </div>
          <b-form-input
            id="token" :type="showtoken ? 'text' : 'password'"
            :value="$store.state.config.bot.token" disabled
          />
        </div>
        <div style="display: flex" class="box flex-row">
          <div class="box-info">
            <span class="info-name">CPU</span>
            <span>{{ $store.state.com.cpu }}</span>
          </div>
          <div class="box-info">
            <span class="info-name">RAM</span>
            <span>{{ $store.state.com.ram }}</span>
          </div>
          <div class="box-info">
            <span class="info-name">PID</span>
            <span>{{ $store.state.com.pid }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      showtoken: false
    }
  },
  mounted () {
    this.$store.commit('setTitle', '봇')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>

<style scoped>
#bot {
  display: flex;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.boxes {
  display: flex;
  flex-direction: column;
}

.box {
  display: inline-block;
  flex-direction: column;
  border-radius: 10px;
  background: #1D2936;
  margin: .5rem;
  padding: 1rem;
  justify-content: center;
}

.status-box {
  width: auto;
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

.botname {
  display: none;
}

.token-box > div {
  display: flex;
}

.token-box > div > span {
  font-size: 1.5rem;
  margin-right: .5rem;
}

#token {
  margin-top: 1rem;
  border-color: gray;
  background: gray;
  color: white;
}

#token::placeholder {
  color: #adb5bd;
}

@media ( min-width: 1350px ) {
  .boxes {
    display: flex;
    flex-direction: row;
  }

  .status-box {
    width: 400px;
  }

  #token {
    min-width: 40rem;
  }

  .profile {
    font-size: 3rem;
  }

  .botname {
    display: inline;
    font-weight: normal;
    margin-left: .5rem;
    font-size: 1.5rem;
  }

  .box-info {
    font-size: 2rem;
  }
}
</style>
