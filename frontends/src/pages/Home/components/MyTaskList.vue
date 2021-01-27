<template>
  <div class="goTop">
    <el-breadcrumb
      separator-class="el-icon-arrow-right"
      style="font-size:16px;margin-top: 5px;"
    >
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item
        :to="{ path: '/task/', query: { type: this.paramtype } }"
        >任务列表</el-breadcrumb-item
      >
      <el-breadcrumb-item
        >MCL列表 -- {{ this.qahead.fobjectid }}</el-breadcrumb-item
      >
    </el-breadcrumb>

    <el-row style="margin-top:20px">
      <el-col :span="24">
        <div style="text-align:right;margin-right:40px">
          <el-button-group>
            <el-button v-show="paramtype === 'approval'" @click="resultApproval()">审核</el-button>
            <el-button v-show="paramtype === 'confirm'" @click="resultRollback()">结果回退</el-button>
            <el-button v-show="paramtype === 'confirm'" @click="resultConfirm()">确认</el-button>
          </el-button-group>
        </div>
      </el-col>
    </el-row>
    <el-table
      :data="qadetails"
      tooltip-effect="dark"
      border
      size="medium"
      style="width: 98%; margin-top:5px"
    >
      <el-table-column label="序号" type="index" width="50"> </el-table-column>
      <el-table-column
        prop="fclass1"
        label="分类"
        width="100"
        show-overflow-tooltip
      >
      </el-table-column>
      <el-table-column prop="fregression" label="回归？" width="70">
        <template slot-scope="scope">
          <el-tag :type="regressionTag" disable-transitions>{{
            scope.row.fregression
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="fapproval" label="状态" width="70">
      </el-table-column>
      <el-table-column prop="fcontent" label="测试用例" show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="ftestdte"
        label="测试日"
        width="100"
      ></el-table-column>
      <el-table-column
        prop="ftestusr"
        label="测试者"
        width="100"
      ></el-table-column>
      <el-table-column
        prop="fresult"
        label="结果"
        width="100"
        :filters="[
          { text: 'NULL', value: null },
          { text: 'OK', value: 'OK' },
          { text: 'NG', value: 'NG' },
          { text: 'NGOK', value: 'NGOK' },
          { text: 'CANCEL', value: 'CANCEL' },
        ]"
        :filter-method="filterResult"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="handleTag(scope.row.fresult)">{{
            scope.row.fresult
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="贴图" width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            style="margin-left:15px"
            v-show="scope.row.fcontent_text.length > 0"
            @click="handleContentText(scope.row.id)"
            >已贴图</el-link
          >
        </template>
      </el-table-column>
    </el-table>

    <el-backtop target=".goTop" :bottom="100">
      <i class="el-icon-caret-top"></i>
    </el-backtop>
  </div>
</template>

<script>
import {
  getQaHead,
  getQaDetailByQaHead,
  updateQaHead,
} from "./../../../services/qaService";
export default {
  data() {
    return {
      paramtype: "",
      parentroute: "",
      qahead: {},
      qadetails: [],
    };
  },

  methods: {
    handleTag(result) {
      if (!result) {
        return "";
      } else if (result === "OK" || result === "NGOK") {
        return "success";
      } else if (result === "NG") {
        return "danger";
      } else {
        return "info";
      }
    },

    handleContentText(id){
      this.$router.push({name: "QaContentText",query:{qadf_id:id}})
    },

    async resultApproval() {
      this.qahead.fstatus = "2";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("审核异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("审核成功");
      }
    },

    async resultRollback() {
      this.qahead.fstatus = "2";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("结果回退异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("结果回退成功");
      }
    },

    async resultConfirm() {
      this.qahead.fstatus = "4";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("结果确认异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("结果确认成功");
      }
    },

    async resultApprovalRollback() {
      this.qahead.fstatus = "1";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("撤销审核异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("撤销审核成功");
      }
    },

    filterResult(value, row) {
      return row.fresult === value;
    },

    async refreshQaList() {
      var resp = await getQaDetailByQaHead(this.qahead.id).catch(() => {
        this.$message.error("测试项数据获取异常");
      });
      if (resp.status === 200) {
        var qadata = resp.data;
        for (var i in qadata) {
          if (qadata[i].fregression === "Y") {
            qadata[i].fregression = "是";
            this.regressionTag = "";
          } else {
            qadata[i].fregression = "否";
            this.regressionTag = "info";
          }
          if (qadata[i].fapproval === "Y") {
            qadata[i].fapproval = "已审核";
            this.approvalTag = "";
          } else {
            qadata[i].fapproval = "未审核";
            this.approvalTag = "info";
          }
        }
        this.qadetails = resp.data;
      }
    },
  },
  mounted: async function() {
    var id = this.$route.query.qahf_id;
    this.paramtype = this.$route.query.type;
    this.parentroute = this.$route.path.split("/")[1];

    var resp = await getQaHead(id).catch(() => {
      this.$message.error("测试对象数据获取异常");
    });
    if (resp.status === 200) {
      this.qahead = resp.data;
      this.refreshQaList();
    }
  },
};
</script>

<style>
.goTop {
  height: calc(100vh - 70px);
  overflow-x: hidden;
}
.el-table--medium td,
.el-table--medium th {
  padding: 2px 0px;
}
.el-table__row {
  height: 20px;
}
.el-table__header {
  padding: 0;
}
.body-style {
  padding: 8px 10px;
}
.div-style {
  margin: 0px;
}
</style>
