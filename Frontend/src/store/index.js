import { createStore } from "vuex";
import { login, getinfo } from "~/api/manager";
import { setToken, removeToken } from "~/composables/auth";
const store = createStore({
  state() {
    return {
      // 用户信息
      cdata: "",
      user: {},
      nowuser: "",
      nowuserclass: "",
      // 侧边宽度
      asideWidth: "250px",
      reason: {},
      menus: ["违约申请"],
      ruleNames: [],
    };
  },
  mutations: {
    // 记录用户信息
    SET_USERINFO(state, user) {
      state.user = user;
    },
    // 展开/缩起侧边
    handleAsideWidth(state) {
      state.asideWidth = state.asideWidth == "250px" ? "64px" : "250px";
    },
    SET_MENUS(state, nowuserclass) {
      state.nowuserclass = nowuserclass;
    },
    SET_MENUS(state, menus) {
      state.menus = menus;
    },
    SET_RULENAMES(state, ruleNames) {
      state.ruleNames = ruleNames;
    },
  },
  actions: {
    // 登录
    login({ commit }, { username, password }) {
      return new Promise((resolve, reject) => {
        login(username, password)
          .then((res) => {
            console.log(res);
            setToken(res.token);
            SET_MENUS(res.class);
            resolve(res);
          })
          .catch((err) => reject(err));
      });
    },

    // 退出登录
    logout({ commit }) {
      // 移除cookie里的token
      removeToken();
      // 清除当前用户状态 vuex
      commit("SET_USERINFO", {});
    },
  },
});

export default store;
