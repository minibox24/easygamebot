<template>
  <div id="test">
    <img class="loop" src="@/assets/logo.png" alt="logo">
    <span>Edit <code>src/App.vue</code> and save to reload.</span>
    <a href="https://vuejs.org/">Learn Vue</a>
  </div>
</template>

<script>
export default {
  mounted () {
    this.$store.commit('setTitle', '붸')
    this.$store.commit('setActivate', this.$route.name)
  }
}
</script>

<style>
#test {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10rem;
}

#test > span {
  font-size: 2.5rem;
  margin-top: 2rem;
}

#test > span > code {
  color: white;
}

#test > a {
  font-size: 2rem;
  color: #42b983;
}

#test > a:visited { text-decoration: none; }

.loop {
  animation: rotate 20s linear infinite;
  transform-origin: 50% 50%;
}

@keyframes rotate{
  100% {
    transform: rotate(360deg);
  }
}
</style>
