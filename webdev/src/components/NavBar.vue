<script>
export default {
  name: 'NavBar',
  methods: {
    git () {
      window.open('https://github.com/minibox24/easygamebot')
    },
    goto (name) {
      switch (name) {
        case 'robot':
          this.$router.push('/')
          break
        case 'user':
          this.$router.push('/user')
          break
        case 'settings':
          this.$router.push('/setting')
          break
      }
    }
  }
}
</script>

<style scoped>
#nav {
  display: flex;
  background: #1D2936;
  color: white;
  z-index: 10;
  width: 46px;
  flex-direction: column;
  padding-top: 3rem;
  user-select: none;
}

#navtitle {
  display: none;
}

.activate-color {
  color: #42B983
}

.nav-box {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 46px;
  cursor: pointer;
}

.nav-box:hover {
  background: #4E6D8D;
}

.nav-box > img {
  width: 24px;
}

.nav-box > span {
  display: none;
}

#gitbutton {
  margin-top: auto;
  margin-bottom: 1rem;
}

@media ( min-width: 1350px ) {
  #nav {
    width: 180px;
    padding-top: 0;
    text-align: center;
  }

  #navtitle {
    display: inline-block;
    margin-top: 2rem;
    margin-bottom: 2rem;
    font-size: 1.25rem;
    font-weight: bold;
  }

  .nav-box {
    justify-content: left;
    padding-left: 1.5rem;
  }

  .nav-box > span {
    margin-left: .5rem;
    display: initial;
  }
}

</style>

<template>
  <div id="nav">
    <span id="navtitle">EasyGameBot</span>
    <div class="nav-box" v-b-tooltip.v-light.hover.right="'봇'" v-on:click="goto('robot')">
      <img :src="this.$store.state.icons.robot" alt="robot">
      <span :class="{ 'activate-color': this.$store.state.activate === 'robot' }">봇</span>
    </div>
    <div class="nav-box" v-b-tooltip.v-light.hover.right="'유저'" v-on:click="goto('user')">
      <img :src="this.$store.state.icons.user" alt="user">
      <span :class="{ 'activate-color': this.$store.state.activate === 'user' }">유저</span>
    </div>
    <div class="nav-box" v-b-tooltip.v-light.hover.right="'설정'" v-on:click="goto('settings')">
      <img :src="this.$store.state.icons.settings" alt="settings">
       <span :class="{ 'activate-color': this.$store.state.activate === 'settings' }">설정</span>
    </div>
    <div
      id="gitbutton" v-on:click="git"
      class="nav-box" v-b-tooltip.v-light.hover.right="'Github'"
    >
      <img src="@/assets/github.svg" alt="github">
      <span>Github</span>
    </div>
  </div>
</template>
