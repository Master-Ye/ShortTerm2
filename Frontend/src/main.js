import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";
import { router } from "./router";
import store from "./store";
import "./assets/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
const app = createApp(App);
app.use(store);
app.use(router);
import { Quasar } from "quasar";
import "@quasar/extras/material-icons/material-icons.css";

// Import Quasar css
import "quasar/dist/quasar.css";
app.use(ElementPlus);
app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
});
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}
import "virtual:windi.css";

import "./permission";

import "nprogress/nprogress.css";

app.mount("#app");
