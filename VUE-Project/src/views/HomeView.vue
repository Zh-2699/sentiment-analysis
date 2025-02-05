<template>
  <div class="home-page">
    <!-- 搜索框 -->
    <div class="search-bar" :class="{ 'sticky-search': isSticky}">
      <input type="text" placeholder="搜索舆情数据..." />
      <button>搜索</button>
    </div>

    <!-- 核心功能入口 -->
    <h1>快速开始</h1>
    <div class="function-cards">
      <div class="card">
        <i class="fas fa-spider"></i>
        <h3>爬取数据</h3>
      </div>
      <div class="card">
        <i class="fas fa-file-alt"></i>
        <h3>文章分析</h3>
      </div>
      <div class="card">
        <i class="fas fa-bell"></i>
        <h3>舆情监控</h3>
      </div>
      <div class="card">
        <i class="fas fa-database"></i>
        <h3>数据管理</h3>
      </div>
    </div>

    <!-- 数据概览 -->
    <h1>数据概览</h1>
    <div class="data-overview">
      <div class="sentiment-distribution">
        <h3>情感分布</h3>
        <div class="charts placeholder">情感分布图表即将呈现</div>
      </div>
      <div class="chart">
        <h3>舆情趋势</h3>
        <div class="charts placeholder">舆情趋势图表即将呈现</div>
      </div>
      <div class="hot-topics" @click="toHotTopicsAnaylsis(hotTopics)">
        <h3><i class="fas fa-fire"> 热点话题 TOP10</i></h3>
        <ol>
          <li v-for="(topic, index) in hotTopics.slice(0, 10)" :key="index">
            <span class="rank">{{ index + 1 }}</span>
            <span class="topic-text">{{ topic.word || topic.note }} .... {{ topic.num }}</span> 
            <span class="topic-num"></span> 
            <img v-if="topic.icon" :src="topic.icon" alt="" class="topic-icon">
          </li>
        </ol>
      </div>
    </div>

    <!-- 最新舆情文章 -->
    <h1>最新舆情文章</h1>
    <div class="realtime-updates">
      <h3>最新舆情文章</h3>
      <ul>
        <li>文章1：舆情热点分析</li>
        <li>文章2：数据可视化趋势</li>
        <li>文章3：情感分布解读</li>
        <li>文章4：舆情监测案例</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

export default {
  name: 'HomeView',
  setup(){
    const hotTopics = ref([]); // 热点话题数据
    const getHotSearch = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/hotSearch')
        console.log(response)
        if (response.status === 200 ){
          hotTopics.value = response.data
          console.log('热搜数据', hotTopics.value)
        }
      } catch (error) {
        console.error('获取热搜失败', error);
      }
    };
    const toHotTopicsAnaylsis = (hotTopics)=>{
      console.log(hotTopics)
    }

    onMounted( ()=>{
      getHotSearch();
    });

    return {
      hotTopics,
      toHotTopicsAnaylsis
    }
  }
}
</script>

<style scoped>
.home-page {
  padding: 20px;
  background-color: rgb(245, 247, 251);
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
}

/* 搜索框样式 */
.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  transition: all 0.3s ease;
}

.sticky-search {
  position: fixed;
  margin-top: 15px;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9;
  padding: 10px;
  width: 80%;
}
.search-bar input {
  width: 60%;
  padding: 12px;
  border: 1px solid #ccc;
  border-right: none;
  border-radius: 5px 0 0 5px;
  font-size: 16px;
}

.search-bar button {
  padding: 12px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.search-bar button:hover {
  background-color: #3aa876;
}

/* 核心功能卡片样式 */
.function-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.function-cards .card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.function-cards .card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.function-cards .card i {
  font-size: 42px;
  color: #42b983;
  margin-bottom: 10px;
}

.function-cards .card h3 {
  font-size: 20px;
  color: #333;
}

/* 数据概览样式对齐调整 */
.data-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.data-overview > div {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.data-overview h3 {
  font-size: 20px;
  color: #333;
}

.charts.placeholder {
  height: 200px;
  border: 2px dashed #ccc;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #999;
}

/* 微博热搜样式 */
.hot-topics {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 400px; /* 固定高度 */
  overflow-y: auto; /* 内容溢出时显示滚动条 */
  cursor: pointer;

  
}
.hot-topics ol {
  list-style: none;
  padding: 0;
  
}

.hot-topics li {
  display: flex;
  align-items: center; /* 竖直居中 */
  justify-content: space-between; /* 内容分布在两端 */
  padding: 10px;
  border-bottom: 1px solid #eee;
  font-size: 18px;
}

.hot-topics .rank {
  font-weight: bold;
  color: #e74c3c;
  margin-right: 10px;
}
.hot-topics .topic-text {
  flex: 1;
  margin-right: 10px; 
}
.hot-topics .topic-num {
  /* font-weight: bold; */
  /* margin-left: 10px;  */
  margin-right: 10px ;
}


.hot-topics li:last-child {
  border-bottom: none;
}
.hot-topics h3{
  color: #e74c3c;
  margin-left: 10px;
}
.topic-icon {
  width: 24px;
  height: 24px;
  object-fit: cover;
}

/* 实时动态样式 */
.realtime-updates {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px 20px 0 20px;
  width: 64%;
  height: 226px;
  overflow-y: auto; /* 内容溢出时显示滚动条 */
}

.realtime-updates h3 {
  font-size: 20px;
  color: #333;
}

.realtime-updates ul {
  list-style: none;
  padding: 0;
}

.realtime-updates ul li {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  font-size: 16px;
}

.realtime-updates ul li:last-child {
  border-bottom: none;
}
</style>
