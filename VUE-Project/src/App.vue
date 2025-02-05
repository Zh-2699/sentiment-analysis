<template>
  <div id="app">
    <div class="main-container">
      <!-- 侧边栏 -->
      <Sidebar />

      <!-- 右侧内容区域 -->
      <div class="content-container">
        <!-- 顶部导航栏 -->
        <TopNavbar />

        <!-- 视图内容 -->
        <router-view class="router-view" />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import TopNavbar from './components/TopNavbar.vue'

export default {
  name: 'App',
  components: {
    Sidebar,
    TopNavbar
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  /* overflow-y: hidden; */
}

#app {
  display: flex;
  flex-direction: column; 
  height: 100vh; 
  overflow: hidden;
}

.main-container {
  display: flex;
  height: 100%;
  overflow: hidden; 
}

.content-container {
  display: flex;
  flex-direction: column;
  flex: 1; 
}

.router-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto; 
  box-sizing: border-box;
}


</style>