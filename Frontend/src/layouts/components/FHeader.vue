<template>
  <div class="f-header z-999">
    <span class="logo">
      <el-icon class="mr-1">
        <eleme-filled />
      </el-icon>
      违约管理
    </span>
    <el-icon class="icon-btn" @click="$store.commit('handleAsideWidth')">
      <fold v-if="$store.state.asideWidth == '250px'" />
      <Expand v-else />
    </el-icon>
    <el-tooltip effect="dark" content="刷新" placement="bottom">
      <el-icon class="icon-btn" @click="handleRefresh">
        <refresh />
      </el-icon>
    </el-tooltip>

    <div class="ml-auto flex items-center">
      <el-tooltip effect="dark" content="全屏" placement="bottom">
        <el-icon class="icon-btn" @click="toggle">
          <full-screen v-if="!isFullscreen" />
          <aim v-else />
        </el-icon>
      </el-tooltip>

      <el-dropdown class="dropdown" @command="handleCommand">
        <span class="flex items-center text-light-50">
          <el-avatar class="mr-2" :size="25" :src="$store.state.user.avatar" />
          {{ username }}
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="rePassword" v-if="class1"
              >更改启用原因</el-dropdown-item
            >
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>

  <form-drawer ref="formDrawerRef" title="修改启用原因" destroyOnClose @submit="onSubmit">
    <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
      <el-checkbox
        v-for="reason in reasons"
        :key="reason.reason_id"
        :label="reason.rea_detail"
        >{{ reason.rea_detail }}</el-checkbox
      >
    </el-checkbox-group>
  </form-drawer>
</template>
<script setup>
import axios from "axios";
import { ref } from "vue";
import { computed } from "vue";
import FormDrawer from "~/components/FormDrawer.vue";
import { useFullscreen } from "@vueuse/core";
import { useRepassword, useLogout } from "~/composables/useManager";
import { setToken, removeToken } from "~/composables/auth";
import { toast } from "~/composables/util";
const {
  // 是否全屏状态
  isFullscreen,
  // 切换全屏
  toggle,
} = useFullscreen();
const username = computed(() => {
  return localStorage.getItem("user");
});
const class1 = computed(() => {
  return localStorage.getItem("userclass") == 1;
});
const checkAll = ref(false);
const isIndeterminate = ref(true);
const reasons = ref([]);

const { formDrawerRef } = useRepassword();
const onSubmit = () => {
  let reastemp = reasons.value;
  let updatedReasons = [];
  for (let i = 0; i < reastemp.length; i++) {
    const currentObject = reastemp[i];
    const reaDetail = currentObject.rea_detail;
    const updatedObject = { ...currentObject };
    if (checkedCities.value.includes(reaDetail)) {
      updatedObject.on1 = 0;
    } else {
      updatedObject.on1 = 1;
    }
    delete updatedObject.rea_detail;
    updatedReasons.push(updatedObject);
  }
  console.log(updatedReasons);
  axios
    .post("http://localhost:5000/updatereason", updatedReasons)
    .then((response) => {
      toast("修改成功");
    })
    .catch((error) => {
      toast("修改失败", "error");
    });
};

const handleCheckedCitiesChange = (value) => {
  const checkedCount = value.length;
  console.log(checkedCities.value);
  checkAll.value = checkedCount === reasons.value.length;
  isIndeterminate.value = checkedCount > 0 && checkedCount < reasons.value.length;
};
const { handleLogout } = useLogout();
const checkedCities = ref([]);
const handleCommand = (c) => {
  switch (c) {
    case "logout":
      {
        handleLogout();
        localStorage.removeItem("user");
        localStorage.removeItem("userclass");
        removeToken();
      }
      break;
    case "rePassword":
      {
        axios.get("http://localhost:5000/reason").then((res) => {
          reasons.value = res.data;
          checkedCities.value = res.data
            .filter((item) => item.on1 == 0)
            .map((item) => item.rea_detail);
          console.log(checkedCities.value);
        });

        formDrawerRef.value.open();
      }
      break;
  }
};

// 刷新
const handleRefresh = () => location.reload();
</script>
<style>
.f-header {
  @apply flex items-center bg-indigo-700 text-light-50 fixed top-0 left-0 right-0;
  height: 64px;
}

.logo {
  width: 250px;
  @apply flex justify-center items-center text-xl font-thin;
}

.icon-btn {
  @apply flex justify-center items-center;
  width: 42px;
  height: 64px;
  cursor: pointer;
}

.icon-btn:hover {
  @apply bg-indigo-600;
}

.f-header .dropdown {
  height: 64px;
  cursor: pointer;
  @apply flex justify-center items-center mx-5;
}
</style>
