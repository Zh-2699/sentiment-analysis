// store/index.js
import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate'

const store = createStore({
  state: {
    isDarkMode: false,   //主题样式
    selectedArticle: null,   //存储选择的文章
    selectedNav: null, //存储选择的分组
    selectedGroup: '热门'
  },
  mutations: {
    TOGGLE_MODE(state, mode) {
      state.isDarkMode = mode;
    },
    SET_SELECTED_ARTICLE(state, article){
      state.selectedArticle = article;  //设置选中的文章
    },
    CLEAR_SELECTED_ARTICLE(state) {
      state.selectedArticle = null;  // 清除选中的文章
    },
    SET_SELECTED_GROUP(state, group) {
      state.selectedGroup = group;  // 设置选中的分组
    },
  },
  actions: {
    changeMode({ commit }, mode) {
      commit('TOGGLE_MODE', mode);
    },
    setSelectedArticles({ commit },article){
      commit('SET_SELECTED_ARTICLE', article)   // 提交设置选中的文章
    },
    clearSelectedArticle({ commit }) {
      commit('CLEAR_SELECTED_ARTICLE');  // 提交清除选中的文章
    },
    setSelectedGroup({ commit }, group) {
      commit('SET_SELECTED_GROUP', group); // 提交设置选中的分组
    },
  },
  getters: {
    isDarkMode: (state) => state.isDarkMode,
    selectedArticle: (state) => state.selectedArticle,  // 获取当前选中的文章
    selectedGroup: (state) => state.selectedGroup, // 获取当前选中的分组
  },
  plugins: [
    createPersistedState({
        key: 'Fudaheng',
        paths: ['isDarkMode','selectedArticle','selectedGroup'],
        storage: window.localStorage
    })
]
});

export default store;
