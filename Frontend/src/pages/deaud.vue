<template>
  <div>
    <el-tabs type="border-card" class="">
      <el-tab-pane label="违约信息审核">
        <el-table :data="tableData" style="width: 100%; margin: auto">
          <el-table-column type="index" width="50" />
          <el-table-column
            prop="cname"
            label="客户名称"
            width="150"
            header-align="center"
          />

          <el-table-column
            prop="outLevel"
            label="最新外部等级"
            width="150"
            header-align="center"
          />
          <el-table-column
            prop="severe"
            label="违约严重性"
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
          <el-table-column
            prop="reason_id"
            label="违约原因"
            width="150"
            header-align="center"
          >
            <template #header>
              <span> 违约原因 </span>
              <el-icon :size="20" class="cursor-pointer" @click="tip()"
                ><InfoFilled
              /></el-icon>
            </template>
          </el-table-column>

          <el-table-column label="操作">
            <template #default="scope">
              <el-button
                size="small"
                type="success"
                @click="handleCheck(scope.$index, scope.row)"
                >详情</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="违约信息查询">
        <el-table
          :data="tableData1"
          style="width: 100%; margin: auto"
          :cell-style="{ textAlign: 'center' }"
          :default-sort="{ prop: 'app_time', order: 'descending' }"
        >
          <el-table-column type="index" width="50">
            <template #header>
              <el-icon class="cursor-pointer" @click="refresh()">
                <RefreshLeft />
              </el-icon> </template
          ></el-table-column>

          <el-table-column
            prop="cname"
            label="客户名称"
            width="150"
            header-align="center"
          />
          <el-table-column
            prop="check_acc"
            label="认定人"
            width="150"
            header-align="center"
          />

          <el-table-column
            prop="app_time"
            label="认定申请时间"
            width="150"
            header-align="center"
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
          <el-table-column
            prop="reason_id"
            label="认定违约原因"
            width="150"
            header-align="center"
          >
            <template #header>
              <span> 认定违约原因 </span>
              <el-icon :size="20" class="cursor-pointer" @click="tip()"
                ><InfoFilled
              /></el-icon>
            </template>
          </el-table-column>
          <el-table-column label="审核状态" prop="s" header-align="center">
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <el-dialog v-model="dialogFormVisible" title="申请详情">
      <h3 class="font-bold">客户名称：{{ nowName }}</h3>
      <h3 class="font-bold">严重程度:{{ nowsevere }}</h3>
      <h3 class="font-bold">备注:{{ nowBeizhu }}</h3>

      <div>附件：<el-button type="error" @click="read()">查看文件</el-button></div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="refuse()" large>拒绝</el-button>
          <el-button type="primary" @click="agree()" large> 同意 </el-button>
        </span>
      </template></el-dialog
    >
  </div>
</template>

<script setup>
import { RefreshLeft } from "@element-plus/icons-vue";
import { toast } from "~/composables/util";
const refresh = () => {
  axios
    .get("http://localhost:5000/reallist")
    .then((res) => {
      console.log(res.data);
      tableData1.value = res.data;
      for (let i = 0; i < tableData1.value.length; i++) {
        tableData1.value[i].s = state.value[tableData1.value[i].s];
      }
      for (var i = 0; i < tableData1.value.length; i++) {
        var obj = tableData1.value[i];

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
    })
    .catch((err) => {
      console.log(err);
    });
};
const state = ref({
  0: "未审核",
  1: "已通过",
  2: "已拒绝",
});
import axios from "axios";
import { ref } from "vue";
import { onMounted } from "vue";
import { ElMessageBox } from "element-plus";
import { InfoFilled } from "@element-plus/icons-vue";
const dialogFormVisible = ref(false);
const nowId = ref("");
const handleCheck = (index, row) => {
  nowName.value = row.cname;
  nowsevere.value = row.severe;
  nowBeizhu.value = row.beizhu;
  nowId.value = row.cus_id;
  dialogFormVisible.value = true;
  idd.value = index;
};
const idd = ref("");
const tableData1 = ref([]);
const agree = () => {
  axios
    .post("http://localhost:5000/agreede", {
      cus_id: nowId.value,
      name: localStorage.getItem("user"),
    })
    .then((res) => {
      toast("操作成功", "success");
      tableData.value.splice(idd.value, 1);
    })
    .catch((err) => {
      console.log(err);
      toast("操作失败", "error");
    });
  dialogFormVisible.value = false;
};
const refuse = () => {
  axios
    .post("http://localhost:5000/disagreede", {
      cus_id: nowId.value,
      name: localStorage.getItem("user"),
    })
    .then(() => {
      toast("操作成功", "success");
      tableData.value.splice(idd.value, 1);
    })
    .catch((err) => {
      toast("操作失败", "error");
    });
  dialogFormVisible.value = false;
};
const read = () => {
  const formData = new FormData();
  formData.append("id", nowId.value);
  axios
    .post("http://localhost:5000/pdf", formData, { responseType: "blob" })
    .then(function (response) {
      // 创建一个新的 FileReader 对象
      var reader = new FileReader();
      console.log(response);
      // 将接收到的数据转换为文件对象
      reader.onloadend = function () {
        // 获取转换后的文件对象
        var file = new File([reader.result], "your_filename.pdf", {
          type: "application/pdf",
        });

        // 处理文件对象，例如展示在界面上或下载
        // ...

        // 示例：使用 window.open() 方法打开 PDF 文件
        var url = URL.createObjectURL(file);
        window.open(url);
      };

      // 读取接收到的数据
      reader.readAsArrayBuffer(response.data);
    })
    .catch(function (error) {
      toast("打开文件失败", "error");
    });
};
onMounted(async () => {
  await axios
    .get("http://localhost:5000/aud2list")
    .then((res) => {
      console.log(res.data);
      let temp = res.data.filter((item) => {
        return item.s === 0 && item.c_or_w === 0;
      });
      for (var i = 0; i < temp.length; i++) {
        var obj = temp[i];

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
      tableData.value = temp;
    })
    .catch((err) => {
      console.log(err);
    });
  await axios
    .get("http://localhost:5000/reallist")
    .then((res) => {
      console.log(res.data);
      tableData1.value = res.data;
      for (let i = 0; i < tableData1.value.length; i++) {
        tableData1.value[i].s = state.value[tableData1.value[i].s];
      }
      for (var i = 0; i < tableData1.value.length; i++) {
        var obj = tableData1.value[i];

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
    })
    .catch((err) => {
      console.log(err);
    });
});
const nowName = ref("");
const nowsevere = ref("");
const nowBeizhu = ref("");

const filterTag = (value, row) => {
  return row.severe === value;
};
const tip = () => {
  ElMessageBox.alert(
    "原因简写 <br/>1:6 个月内，交易对手技术性或资金等原因，给当天结算带来头寸缺口 2 次以上.<br/>2:6 个月内因各种原因导致成交后撤单 2 次以上.<br/>3:未能按照合约规定支付或延期支付利息，本金或其他交付义务（不包括在宽限期内延期支付）.<br/>4:关联违约:集团（内部联系较紧密的集团）或集团内任一公司（较重要的子公司，一旦发生违约会对整个集团造成较大影响的）发生违约.<br/>5:发生消极债务置换：债务人提供给债权人新的或重组的债务，或新的证券组合、现金或资产低于原有金融义务<br/>5:申请破产保护，发生法律接管，或者处于类似的破产保护状态.<br/>6:在其他金融机构违约（包括不限于：人行征信记录中显示贷款分类状态不良类情况，逾期超过 90 天等），或外部评级显示为违约.",
    "说明",
    {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: "我懂了",

      dangerouslyUseHTMLString: true,
    }
  );
};
const tableData = ref([
  {
    reason: 1,
    date: "2016-05-03",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "高",
  },
  {
    date: "2016-05-02",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "高",
  },
  {
    date: "2016-05-04",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "高",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "高",
  },
  {
    date: "2016-05-08",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "低",
  },
  {
    date: "2016-05-06",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    severe: "中",
  },
]);
</script>
