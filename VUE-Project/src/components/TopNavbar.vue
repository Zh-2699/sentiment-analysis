<template>
  <div class="top-navbar" :class="{ darkMode: isDarkMode }">
    <!-- 左侧菜单按钮 -->
    <div class="nav-item" @click="toggleProfile">
      <i class="fas fa-bars"></i>
    </div>
    
    <!-- 右侧夜间模式切换和用户信息 -->
    <div class="right-section">
      <div class="theme-switch">
        <!-- 白天模式按钮 -->
        <button
          class="light-mode"
          :class="{ active: !isDarkMode }"
          @click="changeMode(false)"
        >
          <i class="fas fa-sun"></i>
        </button>
        
        <!-- 黑夜模式按钮 -->
        <button
          class="dark-mode"
          :class="{ active: isDarkMode }"
          @click="changeMode(true)"
        >
          <i class="fas fa-moon"></i>
        </button>
      </div>
      <span class="user-info">{{ user.name }}</span>
    </div>

    <!-- 个人信息弹出框 -->
    <div class="profile-popup" :class="{ active: showProfile }">
    <div class="profile-content">
      <div class="profile-header">
        <h3>个人信息</h3>
        <button @click="toggleProfile" class="close-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>
    <div class="profile-body">
      <p><strong>用户名：</strong>{{ user.name }}</p>
      <p><strong>邮箱：</strong>{{ user.email }}</p>
      <p><strong>电话号码：</strong>{{ user.phoneNumber }}</p>
    </div>
  </div>
</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { computed } from 'vue';

//使用vuex
const store = useStore();
const isDarkMode = computed(() => store.state.isDarkMode);

// 响应式数据：用户信息和夜间模式状态
const user = ref({
  name: 'John Cena',
  email:'John.cena@example.com',
  phoneNumber: '18045032031'
});

// 控制弹出框显示状态
const showProfile = ref(false);

// 切换模式的函数
const changeMode = (mode) => {
  store.dispatch('changeMode', mode);
};

// 切换弹出框显示状态
const toggleProfile = () => {
  showProfile.value = !showProfile.value;
};
</script>

<style scoped>
/* 顶部导航栏样式 */
.top-navbar {
  width: 100%;
  height: 80px;
  background-color: white;
  color: black;
  display: flex;
  justify-content: space-between; 
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 3px 8px -2px rgba(0, 0, 0, 0.15);
  z-index: 10;
  transition: background-color 0.3s ease, color 0.3s ease;
  position: relative; /* 确保弹出框相对于导航栏定位 */
}

/* 夜间模式的样式 */
.darkMode {
  background-color: #2c3e50;
  color: white;
}

/* 左侧导航按钮 */
.nav-item {
  color: #3f476e;
  text-decoration: none;
  font-size: 24px;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  cursor: pointer; /* 添加鼠标指针样式 */
}

.nav-item:hover {
  background-color: #e0e0e0;
}

/* 右侧内容样式 */
.right-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.darkMode .nav-item i {
  color: white;
}

/* 夜间模式切换按钮 */
.theme-switch {
  display: flex;
  align-items: center;
  border: 1px solid #d1d1d1;
  border-radius: 20px;
  overflow: hidden;
  background-color: #f0f0f0;
  transition: background-color 0.3s ease;
}

.darkMode .theme-switch {
  background-color: #34495e;
  border-color: #2c3e50;
}

.theme-switch button {
  border: none;
  background: none;
  padding: 10px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 白天模式按钮 */
.light-mode {
  color: #2c3e50;
  border-radius: 20px 0 0 20px;
}

.light-mode.active {
  background-color: #2c3e50;
  color: white;
}

/* 黑夜模式按钮 */
.dark-mode {
  color: #2c3e50;
  border-radius: 0 20px 20px 0;
}

.dark-mode.active {
  background-color: white;
  color: #2c3e50;
}

/* 禁用激活状态下的 hover 效果 */
.theme-switch button:not(.active):hover {
  background-color: #e0e0e0;
}

.darkMode .theme-switch button:not(.active):hover {
  background-color: #3f476e;
}

/* 用户信息样式 */
.user-info {
  font-size: 16px;
  color: black;
  margin-left: 30px;
  margin-right: 30px;
  transition: color 0.3s ease;
}

.darkMode .user-info {
  color: white;
}

.darkMode .light-mode {
  background-color: #0d2135;
  color: white;
}

/* 个人信息弹出框样式 */
.profile-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保弹出框在最上层 */
  opacity: 0; /* 初始透明度为 0 */
  visibility: hidden; /* 初始不可见 */
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.profile-popup.active {
  opacity: 1; /* 显示时透明度为 1 */
  visibility: visible; /* 显示时可见 */
}

.profile-content {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  width: 350px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-20px); /* 初始位置向上偏移 */
  transition: transform 0.3s ease, opacity 0.3s ease;
  opacity: 0; /* 初始透明度为 0 */
}

.profile-popup.active .profile-content {
  transform: translateY(0); /* 显示时回到原位 */
  opacity: 1; /* 显示时透明度为 1 */
}

.darkMode .profile-content {
  background-color: #2c3e50;
  color: white;
}

/* 弹出框头部样式 */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.darkMode .profile-header {
  border-bottom-color: #3f476e;
}

.profile-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #3f476e;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #e74c3c; /* 悬停时变为红色 */
}

.darkMode .close-btn {
  color: white;
}

.darkMode .close-btn:hover {
  color: #e74c3c;
}

/* 弹出框内容样式 */
.profile-body {
  padding: 10px 0;
}

.profile-body p {
  margin: 15px 0;
  font-size: 16px;
  line-height: 1.6;
}

.profile-body strong {
  font-weight: 600;
  color: #3f476e;
}

.darkMode .profile-body strong {
  color: #42b983;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-content {
    width: 90%;
    padding: 20px;
  }

  .profile-header h3 {
    font-size: 18px;
  }

  .profile-body p {
    font-size: 14px;
  }
}

.darkMode .profile-content {
  background-color: #2c3e50;
  color: white;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.profile-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #3f476e;
}

.darkMode .close-btn {
  color: white;
}

.profile-body p {
  margin: 10px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-info {
    display: none;
  }
}
</style>