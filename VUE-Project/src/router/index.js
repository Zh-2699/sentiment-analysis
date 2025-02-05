import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import SettingsView from '../views/SettingsView.vue'
import WeiboArticlesView from '../views/weibo-articles.vue'
import WeiboCommentsView from '../views/weibo-comments.vue'
import WeiboHotTopicsView from '../views/weibo-hot-topics.vue'
import ArticleAnalysis from '../views/article-analysis.vue'
import SentimentAnalysis from '../views/sentiment-analysis.vue'
import HotTopicAnalysis from '../views/hot-topic-analysis.vue'
import CrawingData from '../views/crawling-data.vue'
import CrawingRes from '../views/crawling-results.vue'
import ArticleDataUpdate from '../views/article-data-update.vue'
import DataDelet from '../views/data-delet.vue'
import ProfilePopu from '../components/ProfilePopup.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/weibo-articles', component: WeiboArticlesView},
  { path: '/weibo-comments', component: WeiboCommentsView},
  { path: '/weibo-hot-topics', component: WeiboHotTopicsView},
  {
    path: '/article-analysis/:id?', // 动态参数 id 可选
    name: 'ArticleAnalysis',
    component: ArticleAnalysis,
    props: true, // 自动将 params 转为 props 传递到组件
  },
  { path: '/sentiment-analysis', component: SentimentAnalysis},
  { path: '/hot-topic-analysis', component: HotTopicAnalysis},
  { path: '/crawling-data', component: CrawingData},
  { path: '/crawling-results', component :CrawingRes},
  { path: '/article-data-update', component: ArticleDataUpdate},
  { path: '/data-delet', component: DataDelet},
  { path: '/analytics', component: AnalyticsView },
  { path: '/settings', component: SettingsView },
  { path: '/profile', component: ProfilePopu}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router