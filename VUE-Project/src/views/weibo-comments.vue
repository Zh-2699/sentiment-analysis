<template>
  <div class="comments-container">
    <h1>评论列表</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <!-- 评论展示区域 -->
      <div v-for="comment in comments" :key="comment.articleId" class="comment-card">
        <div class="comment-header">
          <img :src="comment.author_avatar" alt="头像" class="comment-avatar" />
          <div class="comment-author-info">
            <p><strong>{{ comment.author_name }}</strong></p>
            <p><small>{{ comment.author_address }} | {{ comment.author_gender }}</small></p>
          </div>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <div class="comment-meta">
          <span>👍 {{ comment.likes_counts }}</span>
          <span>🗓️ {{ new Date(comment.created_at).toLocaleString() }}</span>
          <span>📄 id: {{ comment.articleId }}</span>
        </div>
        <button class="analysis-button" @click="showArticleDetail($event, comment)">分析</button>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" :class="['pagination',{ fixed:isFixed}]">
        <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
        <span>当前页: {{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
      </div>
    </div>

    <!-- 返回顶部按钮 -->
    <button v-if="showBackToTop" @click="scrollToTop" class="back-to-top">▲ 顶部</button>

  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router';

export default {
  setup() {
    // 使用ref来定义响应式数据
    const comments = ref([]);
    const loading = ref(true);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const showBackToTop = ref(false);
    const isFixed = ref(false)
    const router = useRouter()

    // 获取评论数据
    const getComments = async (page) => {
      try {
        loading.value = true;
        console.log(page )
        const response = await axios.post('http://127.0.0.1:5000/getcomments', { page });
        const data = response.data;
        console.log(data)

        if (data.success) {
          comments.value = data.comment_data;
          // console.log(comments.value)
          totalPages.value = data.total_pages;
          currentPage.value = data.current_page;
          // console.log(totalPages.value - currentPage.value)
        } else {
          console.error("获取评论失败", data.message);
        }
      } catch (error) {
        console.error("请求失败", error);
      } finally {
        loading.value = false;
      }
    };

    // 切换页数
    const changePage = (page) => {
      if (page < 1 || page > totalPages.value) return;
      getComments(page);
    };

    // 滚动到页面顶部
    const scrollToTop = () => {

      const container = document.querySelector('.comments-container');
      container.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    };

    // 监听滚动事件来显示/隐藏返回顶部按钮
    const handleScroll = () => {
      const container = document.querySelector('.comments-container');
      // console.log('触发了')
      // console.log('容器滚动位置：', container.scrollTop);
      // console.log(window.scrollY)
      if (container.scrollTop > 300) {
        
        // console.log('你好')
        showBackToTop.value = true;
      } else {
        
        showBackToTop.value = false;
      }
      if (container.scrollTop < 1350){
        // console.log("哈哈",container.scrollTop)
        isFixed.value = true;
      }else{
        isFixed.value = false;
      }
    };

    // 跳转到文章详情
    const showArticleDetail = (event, comment) => {
        event.stopPropagation();
        router.push({
          name: 'ArticleAnalysis', // 使用路由名称
          params: { id: String(comment.articleId) }, // 确保动态参数 id 是字符串
          query: { data: JSON.stringify(comment) }, // 将对象序列化为字符串传递
      });
    };

    // 页面加载时获取评论数据
    onMounted(() => {
      const container = document.querySelector('.comments-container');
      getComments(totalPages.value);
      container.addEventListener('scroll', handleScroll);
      
    });

    // 组件销毁时移除事件监听器
    onUnmounted(() => {
      // container.removeEventListener('scroll', handleScroll);
    });

    return {
      comments,
      loading,
      currentPage,
      totalPages,
      showBackToTop,
      getComments,
      changePage,
      scrollToTop,
      showArticleDetail,
      isFixed,
    };
  },
};
</script>

<style scoped>
.comments-container {
  padding: 20px;
  background-color: #f5f7fb;
  font-family: 'Arial', sans-serif;
}

h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
}

.loading {
  text-align: center;
  font-size: 16px;
  color: #666;
}

.comment-card {
  background-color: #fff;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  cursor: pointer;
  position: relative;
}

.comment-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-author-info {
  display: flex;
  flex-direction: column;
}

.comment-author-info p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.comment-author-info small {
  font-size: 12px;
  color: #777;
}

.comment-content {
  font-size: 14px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 10px;
}

.comment-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #777;
}

.comment-meta span {
  display: inline-flex;
  align-items: center;
}

.pagination {
  text-align: center;
  margin-top: 20px;
  margin-left: 10px;
}

.pagination button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  margin: 0 5px;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #3aa876;
}

.pagination span {
  font-size: 14px;
  color: #333;
  margin: 0 10px;
}
.pagination.fixed {
  position: fixed;
  bottom: 60px; /* 避免与返回顶部按钮重叠 */
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 水平居中 */
  z-index: 10;
  background-color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-to-top {
  position: fixed;
  bottom: 60px;
  right: 34px;
  padding: 10px 15px;
  background-color: #fff;         /* 白色背景 */
  color: #333;                    /* 文字颜色 */
  border: none;
  border-radius: 5px;             /* 圆形按钮 */
  cursor: pointer;
  font-size: 14px;
  transition: opacity 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;

  /* 阴影效果 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);  /* 给按钮添加阴影 */
}

.back-to-top:hover {
  background-color: #f5f5f5;       /* 悬停时稍微改变背景色 */
  transform: scale(1.1);            /* 悬停时按钮略微放大 */
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2); /* 悬停时加大阴影 */
}

.back-to-top:focus {
  outline: none;                    /* 去掉点击时的焦点框 */
}
.analysis-button {
  position: absolute; 
  right: 40px; /* 距离右边 10px */
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
</style>
