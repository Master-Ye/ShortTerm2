<template>
  <div>
    <el-table :data="tableData" style="width: 100%; margin: auto">
      <el-table-column type="index" width="50" />
      <el-table-column prop="cname" label="客户名称" width="150" header-align="center" />
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
            :type="scope.row.severe === '高' ? 'error' : 'success'"
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
          <span> 违约原因 </span>
          <el-icon :size="20" class="cursor-pointer" @click="tip()"
            ><InfoFilled
          /></el-icon>
        </template>
      </el-table-column>
      <el-table-column label="认定人" prop="check_acc" header-align="center">
      </el-table-column>
      <el-table-column label="认定申请时间" header-align="center" prop="app_time">
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

    <el-dialog v-model="dialogFormVisible" title="申请详情">
      <h3 class="font-bold">客户名称：{{ nowName }}</h3>
      <h3 class="font-bold">严重程度:{{ nowLevel }}</h3>
      <h3 class="font-bold">违约原因:{{ nowreason1 }}</h3>
      <h3 class="font-bold">重生原因:{{ nowreason2 }}</h3>

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
import { toast } from "~/composables/util";
import axios from "axios";
import { ref } from "vue";
import { onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { InfoFilled } from "@element-plus/icons-vue";
const reason = ref([]);
const reason2 = ref([]);
const refuse = () => {
  console.log(nowId.value);
  axios
    .post("http://localhost:5000/disagreere", {
      cus_id: nowId.value,
      name: localStorage.getItem("user"),
    })
    .then(() => {
      toast("操作成功", "success");
      tableData.value.splice(idd.value, 1);
    })
    .catch((err) => {
      console.log(err);
      toast("操作失败", "error");
    });
  dialogFormVisible.value = false;
};
const agree = () => {
  console.log(nowId.value, nowreason2.value);
  axios
    .post("http://localhost:5000/agreere", {
      cus_id: nowId.value,
      name: localStorage.getItem("user"),
      reasonid: nowreasonid.value,
    })
    .then(() => {
      toast("操作成功", "success");
      tableData.value.splice(idd.value, 1);
    })
    .catch((err) => {
      console.log(err);
      toast("操作失败", "error");
    });
  dialogFormVisible.value = false;
};
const nowreasonid = ref("");
const nowId = ref("");
const idd = ref("");
const dialogFormVisible = ref(false);
const handleCheck = (index, row) => {
  let a = row.cus_id;
  let b = temp.value.filter((item) => {
    return item.cus_id === a && item.c_or_w === 1 && item.s === 0;
  });
  idd.value = index;
  let tempid = b[0].rereasonid;
  nowName.value = row.cname;
  nowLevel.value = row.severe;
  nowId.value = row.cus_id;
  nowreasonid.value = row.rereasonid;
  nowreason1.value = reason.value.filter(
    (item) => item.reason_id === row.reason_id
  )[0].rea_detail;
  nowreason2.value = reason2.value.filter((item) => item.rereasonid === tempid)[0].reason;
  dialogFormVisible.value = true;
};
const temp = ref([]);
onMounted(async () => {
  await axios
    .get("http://localhost:5000/aud2list")
    .then((res) => {
      temp.value = res.data;
      console.log(res.data);
      tableData.value = res.data.filter(function (obj) {
        // 检查对象的 c 属性为 0
        return (
          obj.c_or_w === 0 &&
          res.data.some(function (otherObj) {
            // 检查是否存在其他对象的 cusid 与当前对象相同，并且 c 属性为 1
            return (
              otherObj.cus_id === obj.cus_id && otherObj.c_or_w === 1 && otherObj.s === 0
            );
          })
        );
      });
      for (var i = 0; i < table.value.length; i++) {
        var obj = table.value[i];

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
  await axios
    .get("http://localhost:5000/reason")
    .then((res) => {
      console.log(res.data);
      reason.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
  await axios
    .get("http://localhost:5000/reason2")
    .then((res) => {
      reason2.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
});
const nowName = ref("");
const nowLevel = ref("");
const nowreason1 = ref("");
const nowreason2 = ref("");

const filterTag = (value, row) => {
  return row.level === value;
};
const tip = () => {
  ElMessageBox.alert(
    "原因简写 <br/>0:6 个月内，交易对手技术性或资金等原因，给当天结算带来头寸缺口 2 次以上.<br/>1:6 个月内因各种原因导致成交后撤单 2 次以上.<br/>2:未能按照合约规定支付或延期支付利息，本金或其他交付义务（不包括在宽限期内延期支付）.<br/>3:关联违约:集团（内部联系较紧密的集团）或集团内任一公司（较重要的子公司，一旦发生违约会对整个集团造成较大影响的）发生违约.<br/>4:发生消极债务置换：债务人提供给债权人新的或重组的债务，或新的证券组合、现金或资产低于原有金融义务<br/>5:申请破产保护，发生法律接管，或者处于类似的破产保护状态.<br/>6:在其他金融机构违约（包括不限于：人行征信记录中显示贷款分类状态不良类情况，逾期超过 90 天等），或外部评级显示为违约.",
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
    level: "高",
  },
  {
    date: "2016-05-02",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    level: "高",
  },
  {
    date: "2016-05-04",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    level: "高",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    level: "高",
  },
  {
    date: "2016-05-08",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    level: "低",
  },
  {
    date: "2016-05-06",
    name: "Tom",
    state: "California",
    city: "Los Angeles",
    address: "No. 189, Grove St, Los Angeles",
    zip: "CA 90036",
    level: "中",
  },
]);
</script>
