<template>
    <div class="profile-popup">
      <div class="profile-content">
        <div class="profile-header">
          <h3>个人信息</h3>
          <button @click="closePopup" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="profile-body">
          <p><strong>用户名：</strong>{{ user.name }}</p>
          <p><strong>邮箱：</strong>john.cena@example.com</p>
          <p><strong>角色：</strong>管理员</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  // 用户信息
  const user = ref({
    name: 'John Cena'
  });
  
  // 关闭弹出框
  const closePopup = () => {
    router.go(-1); // 返回上一页
  };
  </script>
  
  <style scoped>
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
  }
  
  .profile-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    width: 300px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
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
  
  .profile-body p {
    margin: 10px 0;
  }
  </style>