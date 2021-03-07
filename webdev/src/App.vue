<template>
  <div id="app">
    <div id="content">
      <NavBar/>
      <div style="display: flex; flex: 1; flex-direction: column; height: calc(100vh - 28px);">
        <Title/>
        <div id="view">
          <router-view/>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import Title from '@/components/Title'
import Footer from '@/components/Footer'

export default {
  components: {
    NavBar,
    Title,
    Footer
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

#app {
  display: flex;
  height: 100vh;
  flex-direction: column;
  font-family: 'Noto Sans KR', sans-serif;
  letter-spacing: -1px;
}

#content {
  flex: auto 1 1;
  display: flex;
  color: white;
}

#view {
  height: 100%;
  background: #2C3E50;
  padding: 1rem;
  overflow: auto;
}

#view::-webkit-scrollbar {
  width: 10px;
}

#view::-webkit-scrollbar-track:hover {
  background: #33485A;
}

#view::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 10px 10px #3A5169;
  border-radius: 10px;
  border: solid 3px transparent;
}

#view::-webkit-scrollbar-thumb:hover {
  box-shadow: inset 0 0 10px 10px #5B7F91;
  border-radius: 10px;
  border: solid 3px transparent;
}
</style>
