<template>
  <div class="article-page">
    <!-- 搜索文章 -->
    <div class="search-bar">
      <input type="text" placeholder="搜索文章..." />
      <button>搜索</button>
    </div>

    <!-- 分组选择 -->
    <div class="group-selector">
      <div>
        <label for="group-select">选择文章分组：</label>
        <select v-model="selectedGroup" @change="onGroupChange">
          <option value="" disabled>请选择分组</option>
          <option v-for="group in articleGroups" :key="group.id" :value="group.name">
            {{ group.name }}
          </option>
        </select>
      </div>
      <div class="spider">
        <div class="card" @click="crawData">
          <i class="fas fa-spider"></i>
          <h3>爬取数据</h3>
        </div>
      </div>
    </div>

    <!-- 文章展示区域 -->
    <div class="article-list">
      <h2>{{ selectedGroup }} 文章</h2>
      <ul v-if="displayedArticles.length > 0">
        <li v-for="article in displayedArticles" :key="article.id" @click="toPage(article)">
          <div class="article-header">
            <img :src="article.authorAvatar" alt="avatar" class="article-avatar" />
            <div class="article-author-info">
              <p><strong>{{ article.authorName }}</strong></p>
              <p><small>{{ article.createdAt }} 来自 {{ article.region || '未知'}}</small></p>
            </div>
          </div>
          <p>{{ article.content }}</p>
          <div class="article-meta">
            <span>👍 {{ article.likeNum }}</span>
            <span>💬 {{ article.commentNum }}</span>
            <span>🔄 {{ article.repostsNum }}</span>
          </div>
          <!-- 文章分析按钮 -->
          <button class="analysis-button" @click="analyzeArticle( $event,article)">分析</button>
        </li>
      </ul>
      <p v-else>该分组下暂无文章。</p>

      <!-- 加载更多按钮 -->
      <div v-if="hasMore" class="load-more">
        <button @click="loadMore">加载更多</button>
      </div>
      <p v-else>没有更多文章了。</p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted} from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const articleGroups = ref([]); // 分组数据
const selectedGroup = ref('热门'); // 当前选中的分组
const articles = ref([]); // 所有文章数据
const displayedArticles = ref([]); // 当前显示的文章
const currentPage = ref(1); // 当前页码
const pageSize = ref(10); // 每页显示的文章数量
const hasMore = ref(true); // 是否还有更多文章
const loading = ref(false); // 是否正在加载数据
const router = useRouter()
const store = useStore();


// 获取分组导航数据
const fetchNavData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/article/navdata');
    articleGroups.value = response.data.groups.map(group => ({
      id: group.gid,
      name: group.name,
    }));

    // 如果默认分组为 "热门"，加载文章
    selectedGroup.value = store.getters.selectedGroup || '热门'   //从vuex中获取
    
  } catch (error) {
    console.error('获取导航数据失败', error);
  }
};

// 获取所有文章数据
const fetchArticles = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/article/data', {
      params: { group: selectedGroup.value },
    });
    articles.value = response.data.reverse(); // 保存完整的文章数据
    console.log(articles)
    resetPagination(); // 初始化分页
  } catch (error) {
    console.error('获取文章数据失败', error);
  }
};

// 初始化分页状态
const resetPagination = () => {
  currentPage.value = 1;
  displayedArticles.value = articles.value.slice(0, pageSize.value); // 显示第一页数据
  hasMore.value = articles.value.length > pageSize.value; // 判断是否还有更多数据
};

// 加载更多文章
const loadMore = () => {
  if (!hasMore.value || loading.value) return;

  loading.value = true;
  const startIndex = currentPage.value * pageSize.value;
  const endIndex = startIndex + pageSize.value;

  // 提取下一页数据并追加到当前显示的数据中
  const nextPageArticles = articles.value.slice(startIndex, endIndex);
  displayedArticles.value.push(...nextPageArticles);

  // 更新分页状态
  currentPage.value += 1;
  hasMore.value = articles.value.length > displayedArticles.value.length;
  loading.value = false;
};

// 分组切换时重置状态
const onGroupChange = async () => {
  store.dispatch('setSelectedGroup', selectedGroup.value);  // 更新 Vuex 中的 selectedGroup
  await fetchArticles();  // 更新当前显示的文章
};
// 跳转到文章详情页面
const toPage = (article) => {
  console.log(article);
  //跳转到界面
  // window.location.href = article.detailUrl;
  window.open(article.detailUrl,'_blank');

};
//跳转到文章分析界面
const analyzeArticle = (event ,article) => {
  //阻止事件冒泡
  event.stopPropagation();
  // console.log(article)
  store.dispatch('setSelectedArticles', article);
  router.push('/article-analysis',)
}
//爬取数据
const crawData = async () =>{
  try{
    const response = await axios.post('http://127.0.0.1:5000/article/crawl', {
      group: selectedGroup.value
    });
  if (response.data.success) {
    console.log(response.data)
    alert('数据爬取成功')
    await fetchArticles
  }else{
    alert('爬取失败');
  }
  } catch (error){
    console.log('爬取失败',error)
    alert('爬取数据发生错误')
  }
}

// 初始化
onMounted(async () => {
  await fetchNavData(); // 加载分组数据
  if (selectedGroup.value) {
    await fetchArticles(); // 加载默认分组的文章
  }
});
</script>

<style scoped>
.article-page {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: rgb(245, 247, 251);
}

/* 分组选择器样式 */
.group-selector {
  justify-content:space-between;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
}

.group-selector label {
  font-weight: bold;
  margin-right: 10px;
  color: #333;
  font-size: 16px;
}

.group-selector select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  cursor: pointer;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  width: 200px;
}

.group-selector select:hover {
  border-color: #42b983;
}

.group-selector select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5);
}

/* 文章展示区域样式 */
.article-list {
  padding: 25px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.article-list h2 {
  margin-top: 0;
  font-size: 24px;
  color: #333;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.article-list li{
  position: relative;
  cursor: pointer;


}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s ease;
}

li:last-child {
  border-bottom: none;
}

li:hover {
  background-color: #f9f9f9;
}

li h3 {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;

}

li p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  width: 1500px;
  
}

/* 文章作者信息样式 */
.article-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.article-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.article-author-info {
  display: flex;
  flex-direction: column;
}

.article-author-info p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.article-author-info small {
  font-size: 12px;
  color: #777;
}

.article-meta {
  margin-top: 10px;
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #777;
}

.article-meta span {
  display: inline-flex;
  align-items: center;
}
.analysis-button {
  position: absolute; /* 绝对定位 */
  right: 10px; /* 距离右边 10px */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 完全垂直居中 */
  background-color: #42b983;
  color: white;
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.analysis-button:hover {
  background-color: #3aa876;
}

/* 加载更多按钮样式 */
.load-more {
  text-align: center;
  margin: 20px 0;
}

.load-more button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.load-more button:hover {
  background-color: #3aa876;
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

/* spider样式 */
.spider{
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.spider .card{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background-color: #ffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease box-shadow 0.3s ease;
}
.spider .card i{
  font-size: 24px;
  color: #42b983;
}
/* spider标题 */
.spider .card h3 {
  margin: 0;
  font-size: 16px;
  color:#333
}

.spider .card:hover{
  transform: translateY(-2px);
  background-color: #f9f9f9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.article-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>
