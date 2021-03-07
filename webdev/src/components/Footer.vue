<template>
  <div id="footer">
    <div v-b-tooltip.v-light.hover.top="'봇 상태'"
      class="item status" :class="{
      'color-online': this.$store.state.status,
      'color-offline': !this.$store.state.status,
      'color-error': this.$store.state.status === 2
    }">
      <span>{{ this.$store.state.status ? this.$store.state.status === 2 ? '오류' : '온라인' : '오프라인' }}</span>
    </div>
    <div class="item" v-b-tooltip.v-light.hover.top="'서버 수'">
      <img src="@/assets/server.svg" alt="user">
      <span>{{ this.$store.state.servers }}</span>
    </div>
    <div class="item" v-b-tooltip.v-light.hover.top="'가입 유저 수'">
      <img src="@/assets/userblack.svg" alt="user">
      <span>{{ this.$store.state.users }}</span>
    </div>
    <div class="item item-right"
      v-b-tooltip.v-light.hover.top="'시간'"
    >
      <span>{{ time }}</span>
    </div>
  </div>
</template>

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

<style>
#footer {
  height: 28px;
  background: #42B983;
  display: flex;
  color: #2c3e50;
  user-select: none;
}

.item {
  width: auto;
  margin-left: .5rem;
  padding-left: .5rem;
  padding-right: .5rem;
  cursor: pointer;
}

.item:hover {
  background: #3BA776;
}

.item > img {
  margin-right: .2rem;
}

.status {
  width: 80px;
  color: white;
  text-align: center;
  margin-left: 0;
}

.color-online { background: green; }
.color-online:hover { background: green; }
.color-offline { background: gray; }
.color-offline:hover { background: gray; }
.color-error { background: red; }
.color-error:hover { background: red; }

.item-right {
  margin-left: auto;
}
</style>
