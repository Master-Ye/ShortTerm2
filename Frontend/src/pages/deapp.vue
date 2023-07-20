<template>
  <div>
    <div>
      <el-select v-model="value" class="m-2" placeholder="请选择搜索类别">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-input
        v-model="searchvalue"
        class="w-50 m-2"
        placeholder="请输入搜索内容"
        :prefix-icon="Search"
      />
      <el-button type="primary" @click="search()">搜索</el-button>
      <el-button type="info" @click="clearsearch()">清除搜索</el-button>
    </div>
    <div class="flex justify-between">
      <el-table
        :data="tableData1"
        style="width: 1000px"
        highlight-current-row
        ref="singleTableRef"
        @current-change="handleCurrentChange"
        height="31.25rem"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column type="index" width="100" label="序号" />
        <el-table-column
          prop="cname"
          label="客户名称"
          width="150"
          header-align="center"
        />
        <el-table-column label="最新外部等级" header-align="center" prop="outLevel" />
        <el-table-column label="客户类别" header-align="center">
          <el-table-column
            prop="name"
            label="所在公司"
            width="120"
            header-align="center"
          />
          <el-table-column
            prop="g_game"
            label="所在集团"
            width="120"
            header-align="center"
          />
          <el-table-column
            prop="location"
            label="所在区域"
            width="120"
            header-align="center"
          />

          <el-table-column
            prop="industry"
            label="所在行业"
            width="120"
            header-align="center"
          />
        </el-table-column>
      </el-table>
    </div>
    <div style="margin-top: 1.25rem; width: 1000px">
      <el-button @click="setCurrent()">清除选择</el-button>
      <el-button
        type="success"
        class="float-right"
        @click="currentRow != null ? (dialogFormVisible = true) : toast('请选择一条数据')"
        >提交申请</el-button
      >
    </div>
    <el-dialog v-model="dialogFormVisible" title="违约申请">
      客户名称：<el-input v-model="currentRow.cname" disabled /><br />
      违约原因：
      <el-select
        v-model="currentReason"
        class="m-2"
        placeholder="请选择原因"
        width="600px;"
      >
        <el-option
          v-for="item in reasons"
          :key="item.reason_id"
          :label="item.rea_detail"
          :value="item.reason_id"
        /> </el-select
      ><br />
      备注：<el-input v-model="beizhu" type="textarea" /><br />
      <el-upload
        class="upload-demo mt-7"
        drag
        multiple
        accept=".pdf"
        v-model:file-list="fileList"
        :auto-upload="false"
        :limit="1"
        :show-file-list="true"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">拖拽文件 或<em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip">仅支持pdf格式</div>
        </template>
      </el-upload>
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
import axios from "axios";
const fileList = ref([]);
import { onMounted } from "vue";
import { ref } from "vue";
import { toast } from "~/composables/util";
import { UploadFilled } from "@element-plus/icons-vue";
import { Search } from "@element-plus/icons-vue";
import { ElMessageBox } from "element-plus";
import { useStore } from "vuex";
import { InfoFilled } from "@element-plus/icons-vue";
const store = useStore();
const dialogFormVisible = ref(false);
const currentRow = ref();
const singleTableRef = ref();
const searchvalue = ref("");
const value = ref("");
const beizhu = ref("");
const reasons = ref([{}]);
const currentReason = ref("");
const app = () => {
  if (fileList.value.length == 0 || currentReason.value == "") {
    toast("请填写完整信息", "error");
    return;
  }
  var file = fileList.value[0].raw; // 获取选择的文件
  var formData = new FormData(); // 创建FormData对象
  formData.append("file", file); // 添加文件到FormData对象

  var c_or_w = 0;
  var check_t = 0;
  var s = 0;
  var date = new Date();

  var severe = "高";

  var app_acc = localStorage.getItem("user");
  var check_acc = 0;
  console.log(
    store.state.reason.filter((item) => item.rea_detail == currentReason.value)
  );
  var reason_id = currentReason.value;
  console.log(reason_id);
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
  formData.append("check_t", check_t);
  formData.append("s", s);
  formData.append("severe", severe);
  formData.append("app_time", app_time);
  formData.append("app_acc", app_acc);
  formData.append("check_acc", check_acc);
  formData.append("reason_id", reason_id);
  formData.append("cus_id", cus_id);
  formData.append("beizhu", beizhu.value);
  console.log(formData.get("beizhu"));
  dialogFormVisible.value = false;
  axios
    .post("http://localhost:5000/application", formData)
    .then((response) => response)
    .then((data) => {
      // 处理响应结果
      toast("申请成功", "success");
    })
    .catch((error) => {
      console.error(error);
      toast("申请失败，请联系管理员", "error");
    });
};
onMounted(async () => {
  await axios.get("http://localhost:5000/data").then((res) => {
    store.state.cdata = res.data;
    console.log(res.data);
    tableData.value = res.data.filter((item) => item.ss == 0);
    tableData1.value = tableData.value;
  });
  await axios.get("http://localhost:5000/reason").then((res) => {
    store.state.reason = res.data.filter((item) => item.on1 == 0);
    console.log(store.state.reason);
    reasons.value = res.data.filter((item) => item.on1 == 0);
  });
});
const tableData1 = ref([
  {
    reason: "1",
    date: "2016-05-03",
    name: "AAA",
    class: "California",
    city: "Los Angeles",
    place: "No. 189, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "高",
    ready: "是",
  },
  {
    date: "2016-05-02",
    name: "Tom",
    class: "California",
    city: "Los Angeles",
    place: "199, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "高",
    ready: "否",
  },
  {
    date: "2016-05-04",
    name: "Tom",
    class: "California",
    city: "Los Angeles",
    place: "No. 189, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "高",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    class: "California",
    city: "Los Angeles",
    place: "No. 189, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "高",
  },
  {
    date: "2016-05-08",
    name: "Tom",
    class: "California",
    city: "Los Angeles",
    place: "No. 189, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "低",
  },
  {
    date: "2016-05-06",
    name: "Tom",
    class: "California",
    city: "Los Angeles",
    place: "No. 189, Grove St, Los Angeles",
    industry: "CA 90036",
    level: "中",
  },
]);
const clearsearch = () => {
  tableData1.value = tableData.value;
};
const options = [
  {
    value: "cname",
    label: "客户名称",
  },
  {
    value: "g_game",
    label: "所在集团",
  },

  {
    value: "industry",
    label: "所在行业",
  },
  {
    value: "location",
    label: "所在区域",
  },
];
const setCurrent = (row?: any) => {
  singleTableRef.value!.setCurrentRow(row);
  console.log(currentRow.value);
};
const handleCurrentChange = (val) => {
  currentRow.value = val;
  console.log(currentRow.value);
};
const search = () => {
  tableData1.value = tableData.value.filter((item) =>
    item[value.value].toString().includes(searchvalue.value)
  );
};
const filterTag = (value, row) => {
  return row.level === value;
};

const tableData = ref([]);
</script>
