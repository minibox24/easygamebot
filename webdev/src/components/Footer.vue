<script>
const dayjs = require('dayjs')

export default {
  name: 'Footer',
  data () {
    return {
      time: ''
    }
  },
  mounted () {
    setInterval(this.setTime, 1000)
  },
  methods: {
    setTime () {
      this.time = dayjs().format('YYYY. MM. DD HH:mm:ss')
    }
  }
}
</script>

<style scoped>
#footer {
  height: 28px;
  background: #42B983;
  display: flex;
  color: #2c3e50;
  user-select: none;
}

.footer-item {
  width: auto;
  margin-left: .5rem;
  padding-left: .5rem;
  padding-right: .5rem;
  cursor: pointer;
}

.footer-item:hover {
  background: #3BA776;
}

.footer-item > img {
  margin-right: .2rem;
}

.footer-status {
  width: 80px;
  color: white;
  text-align: center;
  margin-left: 0;
}

.color-online { background: green; }
.color-online:hover { background: green; }
.color-offline { background: gray; }
.color-offline:hover { background: gray; }

.footer-item-right {
  margin-left: auto;
}
</style>

<template>
  <div id="footer">
    <div v-b-tooltip.v-light.hover.top="'봇 상태'"
      class="footer-item footer-status" :class="{
      'color-online': this.$store.state.status,
      'color-offline': !this.$store.state.status
    }">
      <span>{{ this.$store.state.status ? '온라인' : '오프라인' }}</span>
    </div>
    <div class="footer-item" v-b-tooltip.v-light.hover.top="'서버 수'">
      <img src="@/assets/server.svg" alt="user">
      <span>{{ this.$store.state.servers }}</span>
    </div>
    <div class="footer-item" v-b-tooltip.v-light.hover.top="'가입 유저 수'">
      <img src="@/assets/userblack.svg" alt="user">
      <span>{{ this.$store.state.users.length }}</span>
    </div>
    <div class="footer-item footer-item-right"
      v-b-tooltip.v-light.hover.top="'시간'"
    >
      <span>{{ time }}</span>
    </div>
  </div>
</template>
