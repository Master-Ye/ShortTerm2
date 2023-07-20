<template>
  <div class="f-menu" :style="{ width: $store.state.asideWidth }">
    <el-menu
      :default-active="defaultActive"
      unique-opened
      :collapse="isCollapse"
      default-active="2"
      class="border-0"
      @select="handleSelect"
      :collapse-transition="false"
    >
      <el-menu-item index="deapp" v-if="!nowuserclass">
        <el-icon><icon-menu /></el-icon>
        <template #title>违约申请</template>
      </el-menu-item>
      <el-menu-item index="reapp" v-if="!nowuserclass">
        <el-icon><icon-menu /></el-icon>
        <template #title>重生申请</template>
      </el-menu-item>
      <el-menu-item index="deaud" v-if="nowuserclass">
        <el-icon><icon-menu /></el-icon>
        <template #title>违约审核</template>
      </el-menu-item>
      <el-menu-item index="reaud" v-if="nowuserclass">
        <el-icon><icon-menu /></el-icon>
        <template #title>重生审核</template>
      </el-menu-item>
      <el-menu-item index="dataview" v-if="nowuserclass">
        <el-icon><icon-menu /></el-icon>
        <template #title>数据统计</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>
<script setup>
import { computed, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { Document, Menu as IconMenu, Location, Setting } from "@element-plus/icons-vue";
const router = useRouter();
const store = useStore();
const route = useRoute();

// 默认选中
const defaultActive = ref(route.path);
const nowuserclass = computed(() =>
  localStorage.getItem("userclass") == 1 ? true : false
);
const reasons = ref([]);
// 是否折叠
const isCollapse = computed(() => !(store.state.asideWidth == "250px"));

const asideMenus = computed(() => store.state.menus);

const handleSelect = (e) => {
  console.log(e);
  router.push(e);
};
</script>
<style>
.f-menu {
  transition: all 0.2s;
  top: 64px;
  bottom: 0;
  left: 0;
  overflow-y: auto;
  overflow-x: hidden;
  @apply shadow-md fixed bg-light-50;
}
.f-menu::-webkit-scrollbar {
  width: 0px;
}
</style>
