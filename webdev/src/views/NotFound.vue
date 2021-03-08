<template>
  <div id="notfound">
    <h1>별 거 없네요.</h1>
    <span>오신김에 <a id="gitstar" href="https://github.com/minibox24/easygamebot">깃허브 스타</a> 하나만 눌러주세요</span>
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '404 Not Found')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>

<style scoped>
#gitstar {
  text-decoration: none;
  color: #42B983;
}
</style>
