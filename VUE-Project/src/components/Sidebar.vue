<template>
  <div class="sidebar">
    <div class="logo">
      <img src="./../assets/img/4f7626ee9b2ac3ccf32cd8b677db2af.jpg" alt="Logo">
      <span class="logo-text">舆情分析系统</span>
    </div>
    <ul>
      <a class="title">首页</a>
      <li><router-link to="/" class="nav-item"><i class="fas fa-home"></i>首页</router-link></li>
      <li><router-link to="/weibo-articles" class="nav-item"><i class="fas fa-file-alt"></i> 微博文章</router-link></li>
      <li><router-link to="/weibo-comments" class="nav-item"><i class="fas fa-comments"></i> 微博评论</router-link></li>
      <li><router-link to="/weibo-hot-topics" class="nav-item"><i class="fas fa-fire"></i> 微博热门话题</router-link></li>
      <a class="title">数据分析</a>
      <li><router-link to="/article-analysis" class="nav-item"><i class="fas fa-file-contract"></i> 文章分析</router-link></li>
      <li><router-link to="/sentiment-analysis" class="nav-item"><i class="fas fa-chart-pie"></i> 舆情分析</router-link></li>
      <li><router-link to="/hot-topic-analysis" class="nav-item"><i class="fas fa-chart-bar"></i> 热门话题分析</router-link></li>
      <a class="title">数据管理</a>
      <li><router-link to="/crawling-data" class="nav-item"><i class="fas fa-spider"></i> 爬取数据</router-link></li>
      <li><router-link to="/crawling-results" class="nav-item"><i class="fas fa-table"></i> 爬取结果</router-link></li>
      <li><router-link to="/article-data-update" class="nav-item"><i class="fas fa-sync"></i> 文章数据更新</router-link></li>
      <li><router-link to="/data-delet" class="nav-item"><i class="fas fa-trash"></i> 数据删除</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style scoped>
/* 侧边栏样式 */
.sidebar {
  width: 250px; 
  height: 100vh;
  background: linear-gradient(135deg, #2c3e50, #34495e); 
  color: #d1d1d1; 
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3);
  font-family: 'Roboto', Arial, sans-serif;
  overflow-y: auto;
  transition: width 0.3s ease;
}

/* Logo 区域样式 */
.logo {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  margin-bottom: 30px;    
  border-radius: 10px;
}

.logo img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.logo-text {
  color: #d1d1d1;
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  letter-spacing: 1px;
}

/* 导航链接样式 */
.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin: 15px 0;
}

.nav-item {
  color: #d1d1d1; 
  text-decoration: none;
  font-size: 16px;
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.nav-item i {
  margin-right: 10px;
}

/* 悬停效果 */
.nav-item:hover {
  background-color: #3f476e;
  padding-left: 20px;
  transform: translateX(5px);
  color: #f5f5f5; 
}

/* 选中状态的样式 */
.nav-item.router-link-exact-active {
  background-color: #3f476e;
  padding-left: 20px;
  transform: translateX(5px);
  font-weight: bold;
  color: #ffffff; 
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.8); 
  
}

.title {
  margin: 0px;
  font-weight: bold;
  color: #d1d1d1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .content-container {
    margin-left: 0;
  }
}
</style>
