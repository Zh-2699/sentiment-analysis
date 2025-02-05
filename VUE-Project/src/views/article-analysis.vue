<template>
  <div class="article-analysis-page">
    <!-- 标题 -->
    <div class="page-header">
      <h1>文章分析</h1>
    </div>

    <!-- 主体内容 -->
    <div class="analysis-container">
      <!-- 文章内容卡片 -->
      <div v-if="article" class="analysis-card main-article">
        <div class="article-header">
          <img :src="article.authorAvatar" alt="avatar" class="article-avatar" />
          <div class="article-author-info">
            <p><strong>{{ article.authorName }}</strong></p>
            <p><small>{{ formatDate(article.createdAt) }} 来自 {{ article.region || '未知'}}</small></p>
          </div>
        </div>
        <div class="article-content">
          <p>{{ article.content }}</p>
          <div class="article-meta">
            <span>👍 {{ article.likeNum }}</span>
            <span>💬 {{ article.commentNum }}</span>
            <span>🔄 {{ article.repostsNum }}</span>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <p>正在加载评论...</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ error }}</p>
      </div>

      <!-- 评论列表 -->
      <div v-if="!loading && !error" class="comments-section">
        <div class="section-header">
          <h2>评论分析</h2>
          <span class="comment-count">共 {{ comments.length }} 条评论</span>
        </div>

        <div v-if="comments.length > 0" class="comment-list">
          <div v-for="comment in comments" :key="comment.articleId + comment.authorName" class="analysis-card comment-item">
            <div class="comment-header">
              <img :src="comment.author_avatar" alt="avatar" class="comment-avatar" />
              <div class="comment-author-info">
                <p><strong>{{ comment.author_name }}</strong></p>
                <p><small>{{ comment.region }}</small></p>
              </div>
            </div>
            <div class="comment-content">
              <p>{{ comment.content }}</p>
              <div class="comment-meta">
                <span>👍 {{ comment.likes_counts || 0 }}</span>
                <div class="meta-right">
                  <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                  <!-- 新增情感标签 -->
                  <!-- <span class="sentiment-tag sentiment-positive">积极</span> -->
                  <!-- 其他情感状态示例 -->
                  <!-- <span class="sentiment-tag sentiment-neutral">中立</span> -->
                  <span class="sentiment-tag sentiment-negative">消极</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <i class="fas fa-comment-slash"></i>
          <p>暂无评论数据</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

// 获取 Vuex store
const store = useStore();
const route = useRoute(); // 获取路由对象

// 定义响应式数据
const article = ref(null); // 文章信息
const comments = ref([]); // 评论列表
const loading = ref(true); // 加载状态
const error = ref(null); // 错误信息

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // 格式化为本地时间格式
};

// 加载文章
const fetchArticle = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/getArticleById?id=${id}`);
    if (response.data.success) {
      article.value = response.data.article; // 将文章数据赋值给响应式变量
      console.log('文章数据:', response.data.article);
    } else {
      error.value = '加载文章失败';
    }
  } catch (err) {
    error.value = '加载文章失败：' + err.message;
  }
};

// 加载评论
const fetchComments = async (id) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/getcommentsById', {
      articleId: id,
    });
    if (response.data.success) {
      comments.value = response.data.comment_data; // 将评论数据赋值给响应式变量
      console.log('评论数据:', response.data.comment_data);
    } else {
      error.value = '加载评论失败';
    }
  } catch (err) {
    error.value = '加载评论失败：' + err.message;
  } finally {
    loading.value = false; // 加载完成
  }
};

// 初始化
onMounted(async () => {
  const articleId = route.params.id || null; // 获取路由中的文章 ID

  if (articleId) {
    // 如果路由中有文章 ID，从后端加载文章和评论
    await fetchArticle(articleId);
    await fetchComments(articleId);
  } else {
    // 如果路由中没有文章 ID，从 Vuex 获取文章数据
    article.value = store.getters.selectedArticle;

    if (article.value) {
      await fetchComments(article.value.id); // 加载评论
    } else {
      error.value = '没有找到选中的文章数据';
      loading.value = false;
    }
  }
});
</script>

<style scoped>
.article-analysis-page {
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: rgb(245, 247, 251);
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 24px;
  color: #333;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
  display: inline-block;
}

.analysis-container {
  max-width: 1800px;
  margin: 0 auto;
}

/* 卡片通用样式 */
.analysis-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.analysis-card:hover {
  transform: translateY(-2px);
}

/* 文章内容区域 */
.main-article .article-content {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.article-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.article-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
}

.article-author-info p {
  margin: 2px 0;
  font-size: 14px;
}

.article-author-info small {
  color: #777;
  font-size: 12px;
}

.article-content p {
  font-size: 15px;
  color: #333;
  line-height: 1.7;
  margin-bottom: 15px;
}

.article-meta {
  display: flex;
  gap: 20px;
  color: #777;
  font-size: 14px;
  margin-top: 15px;
}

/* 评论区域 */
.comments-section {
  margin-top: 30px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 20px;
  color: #333;
  margin: 0;
}

.comment-count {
  font-size: 14px;
  color: #777;
}

.comment-item {
  margin-bottom: 15px;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.comment-content p {
  font-size: 14px;
  color: #444;
  line-height: 1.6;
  margin: 0 0 10px;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #777;
  font-size: 13px;
  margin-top: 10px;
}

.meta-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sentiment-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 情感颜色方案 */
.sentiment-positive {
  background-color: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
}

.sentiment-neutral {
  background-color: #fff3e0;
  color: #ef6c00;
  border: 1px solid #ffcc80;
}

.sentiment-negative {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ef9a9a;
}

/* 调整时间显示样式 */
.comment-time {
  font-style: italic;
  color: #9e9e9e;
}

/* 状态提示样式 */
.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 40px 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.loading-state i,
.error-state i,
.empty-state i {
  font-size: 32px;
  margin-bottom: 15px;
  color: #42b983;
}

.error-state i {
  color: #ff4757;
}

.empty-state i {
  color: #a4b0be;
}

.loading-state p,
.error-state p,
.empty-state p {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.fa-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}
</style>
