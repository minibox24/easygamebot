<template>
  <div id="app">
    <div id="content">
      <NavBar/>
      <div style="flex: 1">
        <Title/>
        <div id="view">
          <router-view/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import Title from '@/components/Title'

export default {
  components: {
    NavBar,
    Title
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;400;900&display=swap');

#app {
  display: flex;
  flex-direction: column;
  font-family: 'Noto Sans KR', sans-serif;
  overflow: hidden;
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
  box-shadow: inset 0 0 10px 10px #5B7F91;
  border-radius: 10px;
  border: solid 3px transparent;
}
</style>
