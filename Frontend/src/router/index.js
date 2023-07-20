import { createRouter, createWebHashHistory } from "vue-router";

import Admin from "~/layouts/admin.vue";
import Index from "~/pages/index.vue";
import Login from "~/pages/login.vue";
import NotFound from "~/pages/404.vue";
import Reapp from "~/pages/reapp.vue";
import Reaud from "~/pages/reaud.vue";
import Deapp from "~/pages/deapp.vue";
import Deaud from "~/pages/deaud.vue";
import Dataview from "~/pages/dataview.vue";

// 默认路由，所有用户共享
const routes = [
  {
    path: "/main",
    name: "admin",
    component: Admin,
    children: [
      {
        path: "/reapp",
        component: Reapp,
        meta: {
          title: "重生申请",
        },
      },
      {
        path: "/reaud",
        component: Reaud,
        meta: {
          title: "重生审核",
        },
      },
      {
        path: "/deaud",
        component: Deaud,
        meta: {
          title: "违约审核",
        },
      },
      {
        path: "/deapp",
        component: Deapp,
        meta: {
          title: "违约申请",
        },
      },
      {
        path: "/dataview",
        component: Dataview,
        meta: {
          title: "数据统计",
        },
      },
      {
        path: "/:pathMatch(.*)*",
        name: "NotFound",
        component: NotFound,
      },
    ],
  },
  {
    path: "/login",
    component: Login,
    meta: {
      title: "登录页",
    },
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
  },
];

// 动态路由，用于匹配菜单动态添加路由
const asyncRoutes = [
  {
    path: "/",
    name: "/",
    component: Index,
    meta: {
      title: "后台首页",
    },
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 动态添加路由的方法
export function addRoutes(menus) {
  // 是否有新的路由
  let hasNewRoutes = false;
  const findAndAddRoutesByMenus = (arr) => {
    arr.forEach((e) => {
      let item = asyncRoutes.find((o) => o.path == e.frontpath);
      if (item && !router.hasRoute(item.path)) {
        router.addRoute("admin", item);
        hasNewRoutes = true;
      }
      if (e.child && e.child.length > 0) {
        findAndAddRoutesByMenus(e.child);
      }
    });
  };

  findAndAddRoutesByMenus(menus);

  return hasNewRoutes;
}
