<template>
  <div>
    <el-table
      :default-sort="{ prop: 'date', order: 'descending' }"
      :data="tableData"
      style="width: 100%; margin: auto"
      highlight-current-row
      ref="singleTableRef"
      @current-change="handleCurrentChange"
      :cell-style="{ textAlign: 'center' }"
    >
      <el-table-column prop="cname" label="客户名称" width="150" header-align="center" />
      <el-table-column
        prop="reason_id"
        label="认定违约原因"
        width="150"
        header-align="center"
      />
      <el-table-column
        prop="severe"
        label="严重程度"
        width="150"
        header-align="center"
        :filters="[
          { text: '高', value: '高' },
          { text: '中', value: '中' },
          { text: '低', value: '低' },
        ]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.severe === '高' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.severe }}</el-tag
          >
        </template></el-table-column
      >
      <el-table-column prop="check_acc" label="认定人" width="150" header-align="center">
      </el-table-column>
      <el-table-column
        prop="app_time"
        label="认定申请时间"
        width="150"
        header-align="center"
        sortable
      />
      <el-table-column
        prop="check_t"
        label="认定审核时间"
        width="150"
        header-align="center"
      />
      <el-table-column
        prop="outLevel"
        label="最新外部等级"
        width="150"
        header-align="center"
      />
    </el-table>
    <div style="margin-top: 1.25rem; width: 100%">
      <el-button @click="setCurrent()">清除选择</el-button>
      <el-button
        type="success"
        class="float-right"
        @click="
          currentRow != null
            ? (dialogFormVisible = true)
            : toast('请选择一条数据', 'error')
        "
        >提交申请</el-button
      >
    </div>
    <el-dialog v-model="dialogFormVisible" title="重生申请">
      客户名称：<el-input v-model="currentRow.cname" disabled /><br />

      认定人：<el-input v-model="currentRow.check_acc" disabled /><br />
      认定违约原因：<el-input v-model="nowreason" disabled /><br />
      认定申请时间：<el-input v-model="currentRow.app_time" disabled /><br />
      最新外部等级：<el-input v-model="currentRow.outLevel" disabled /><br />
      选择重生原因：

      <el-select v-model="rereason" class="m-2" placeholder="">
        请选择重生原因
        <el-option
          v-for="item in rereasons"
          :key="item.value"
          :label="item.detail"
          :value="item.value"
        />
      </el-select>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="app()" large> 确认申请 </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { useStore } from "vuex";
const store = useStore();
import { computed, onMounted, ref } from "vue";
import axios from "axios";

import { toast } from "~/composables/util";
const dialogFormVisible = ref(false);
onMounted(async () => {
  await axios.get("http://localhost:5000/data1").then((res) => {
    console.log(res.data);
    tableData.value = res.data;
    for (var i = 0; i < tableData.value.length; i++) {
      var obj = tableData.value[i];

      // 检查条件
      if (obj.reason_id > 4) {
        // 添加属性
        obj.severe = "高";
      }
      if (obj.reason_id < 3) {
        // 添加属性
        obj.severe = "低";
      }
      if (obj.reason_id >= 3 && obj.reason_id <= 4) {
        obj.severe = "中";
      }
    }
  });
  await axios.get("http://localhost:5000/reason").then((res) => {
    store.state.reason = res.data.filter((item) => item.on1 == 0);
    console.log(store.state.reason);
    reasons.value = res.data.filter((item) => item.on1 == 0);
    console.log(reasons.value);
  });
});
const idd = ref("");
const rereason = ref("");
const setCurrent = (row?: any) => {
  singleTableRef.value!.setCurrentRow(row);
  console.log(currentRow.value);
};
const handleCurrentChange = (val) => {
  currentRow.value = val;
  console.log(val);
};
const app = () => {
  var formData = new FormData(); // 创建FormData对象

  // 构建其他参数

  var c_or_w = 1;

  var s = 0;
  var date = new Date();

  var severe = "高";

  var app_acc = localStorage.getItem("user");
  var check_acc = 0;
  if (rereason.value == "") {
    toast("请选择重生原因", "error");
    return;
  }
  var reason_id = rereason.value;
  console.log(currentRow.value);
  var cus_id = currentRow.value.cus_id;
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var day = date.getDate();
  var hours = date.getHours();
  month = month < 10 ? "0" + month : month;
  day = day < 10 ? "0" + day : day;
  hours = hours < 10 ? "0" + hours : hours;
  var app_time = year + "-" + month + "-" + day;
  formData.append("c_or_w", c_or_w);
  console.log(reason_id);
  formData.append("s", s);
  formData.append("severe", severe);
  formData.append("app_time", app_time);
  formData.append("app_acc", app_acc);
  formData.append("check_acc", check_acc);
  formData.append("reason_id", reason_id);
  formData.append("cus_id", cus_id);

  console.log(formData.get("cus_id"));
  dialogFormVisible.value = false;
  axios
    .post("http://localhost:5000/application1", formData)

    .then((data) => {
      toast("申请成功", "success");
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
      toast("申请失败", "error");
    });
};
const nowreason = computed(() => {
  return reasons.value.filter((item) => item.reason_id == currentRow.value.reason_id)[0]
    .rea_detail;
});
const currentRow = ref([]);
const singleTableRef = ref();

const filterTag = (value, row) => {
  return row.level === value;
};
const reasons = ref([]);
const rereasons = ref([
  {
    value: 1,
    detail: "正常结算后解除",
  },

  {
    value: 2,
    detail: "在其他金融机构违约解除，或外部评级显示为非违约级别",
  },
  {
    value: 3,
    detail: "计提比例小于设置界限",
  },
  {
    value: 4,
    detail: "连续 12 个月内按时支付本金和利息",
  },
  {
    value: 5,
    detail:
      "客户的还款意愿和还款能力明显好转，已偿付各项逾期本金、逾期利息和其他费用（包括罚息等），且连续 12 个月内按时支付本金、利",
  },
  {
    value: 6,
    detail: "导致违约的关联集团内其他发生违约的客户已经违约重生，解除关联成员的违约设定",
  },
]);

const tableData = ref([
  {
    app_time: "Mon, 03 Jul 2023 00:00:00 GMT",
    check_acc: "king",
    check_t: "Mon, 03 Jul 2023 00:00:00 GMT",
    cname: "zze",
    cus_id: "10006",
    outLevel: "C",
    reason_id: 1,
    severe: "高",
  },
]);
</script>
