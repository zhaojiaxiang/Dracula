<template>
  <div class="goTop">
    <el-row>
      <el-col :span="10"
        ><div>
          <div style="margin:10px">
            <el-page-header @back="goBack"> </el-page-header>
          </div></div
      ></el-col>
      <el-col :span="14">
        <div>
          <MCLTargetActual></MCLTargetActual>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-top:5px">
      <el-col :span="24">
        <div style="text-align:right;margin-right:40px">
          <el-button-group>
            <el-button v-show="isCanApproval()" @click="resultApproval()"
              >审核</el-button
            >
            <el-button v-show="isCanConfirm()" @click="resultRollback()"
              >结果回退</el-button
            >
            <el-button v-show="isCanConfirm()" @click="resultConfirm()"
              >确认</el-button
            >
            <el-button
              v-show="isCanRollbackConfirm()"
              @click="resultRollbackConfirm()"
              >取消确认</el-button
            >
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
      v-loading="loading"
    >
      <el-table-column label="序号" type="index" width="50"> </el-table-column>
      <el-table-column
        prop="fclass1"
        label="分类1"
        width="100"
        show-overflow-tooltip
      >
      </el-table-column>
      <el-table-column
        prop="fclass2"
        label="分类2"
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
            v-show="scope.row.fcontent_text"
            @click="handleContentText(scope.row.id)"
            >{{ scope.row.test_tag }}</el-link
          >
        </template>
      </el-table-column>
    </el-table>

    <QaConfirm @confirmed="confirmed()" ref="QaConfirm"></QaConfirm>

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
import QaConfirm from "../../Home/components/QaConfirm";
import MCLTargetActual from "../../Home/components/MCLTargetActual";
export default {
  components: {
    QaConfirm,
    MCLTargetActual,
  },
  data() {
    return {
      loading: false,
      qaheadId: "",
      qahead: {},
      qadetails: [],
    };
  },

  methods: {
    goBack() {
      window.history.go(-1);
    },
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

    isCanApproval() {
      for (var i in this.qadetails) {
        if (this.qadetails[i].fapproval === "未审核") {
          return true;
        }
      }
      return false;
    },

    isCanConfirm() {
      if (this.qahead.fstatus === "3") {
        return true;
      }
      return false;
    },

    isCanRollbackConfirm() {
      if (this.qahead.fstatus === "4") {
        return true;
      }
      return false;
    },

    confirmed() {
      this.refreshQaList();
    },

    handleContentText(id) {
      this.$router.push({
        name: "QaContentText",
        query: { type: "approval", qadf_id: id },
      });
    },

    async resultRollbackConfirm() {
      this.$confirm("此操作将取消确认该对象, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            this.qahead.fstatus = "3";
            var resp = await updateQaHead(this.qahead.id, this.qahead).catch(
              () => {
                this.$message.error("取消确认异常");
              }
            );
            if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
              this.$message.error(resp.data.message);
            } else {
              this.$message.success("取消确认成功");
              this.refreshQaList();
            }
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "操作取消",
          });
        });
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
        this.refreshQaList();
      }
    },

    async resultRollback() {
      this.$confirm("此操作将回退该对象测试结果, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            this.qahead.fstatus = "2";
            var resp = await updateQaHead(this.qahead.id, this.qahead).catch(
              () => {
                this.$message.error("结果回退异常");
              }
            );
            if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
              this.$message.error(resp.data.message);
            } else {
              this.$message.success("结果回退成功");
              this.refreshQaList();
            }
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "操作取消",
          });
        });
    },

    resultConfirm() {
      this.$refs.QaConfirm.handleDialog(this.qahead.id);
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
        this.refreshQaList();
      }
    },

    filterResult(value, row) {
      return row.fresult === value;
    },

    async refreshQaList() {
      var resp_head;
      resp_head = await getQaHead(this.qaheadId).catch(() => {
        this.$message.error("测试对象数据获取异常");
      });

      if (Object.prototype.hasOwnProperty.call(resp_head.data, "message")) {
        this.$message.error(resp_head.data.message);
      }

      this.qahead = resp_head.data;

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
    this.loading = true;
    this.qaheadId = this.$route.query.qahf_id;
    this.refreshQaList();
    this.loading = false;
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
