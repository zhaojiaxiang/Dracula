<template>
  <div class="goTop">
    <el-row>
      <el-col :span="10"
        ><div>
          <el-breadcrumb
            separator-class="el-icon-arrow-right"
            style="font-size:16px;margin-top: 5px;"
          >
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item
              v-show="paramtype !== 'mcl'"
              :to="{ path: '/qa/', query: { slipno: this.qahead.fslipno } }"
              >QA列表</el-breadcrumb-item
            >
            <el-breadcrumb-item
              v-show="paramtype === 'mcl'"
              :to="{ path: '/task/', query: { type: this.paramtype } }"
              >任务列表</el-breadcrumb-item
            >
            <el-breadcrumb-item
              >MCL列表 -- {{ this.qahead.fobjectid }}</el-breadcrumb-item
            >
          </el-breadcrumb>
        </div></el-col
      >
      <el-col :span="14">
        <div>
          <MCLTargetActual ref="MCLTargetActual"></MCLTargetActual>
        </div>
      </el-col>
    </el-row>

    <el-row style="margin-top:5px">
      <el-col :span="12">
        <div>
          <el-button
            type="danger"
            :disabled="isCanBatchDelete()"
            v-loading.fullscreen.lock="fullscreenLoading"
            @click="batchDeleteQaDetail()"
            >删除选中项</el-button
          >
        </div>
      </el-col>
      <el-col :span="12">
        <div style="text-align:right;margin-right:40px">
          <el-button-group>
            <el-button @click="defaultOK()" v-show="isCanDefaultOK()"
              >Default OK</el-button
            >
            <el-button @click="detailModify()">修改明细</el-button>
            <el-button v-show="isCanAdd()" @click="singleAdd()"
              >逐条添加</el-button
            >
            <el-button v-show="isCanAdd()" @click="batchAdd()"
              >批量添加</el-button
            >
            <el-button
              type="primary"
              v-show="isCanSubmit()"
              @click="resultSubmit()"
              >提交结果</el-button
            >
            <el-button v-show="isCanRoback()" @click="resultRollback()"
              >结果撤回</el-button
            >
          </el-button-group>
        </div>
      </el-col>
    </el-row>
    <el-table
      ref="multipleTable"
      :data="qadetails"
      tooltip-effect="dark"
      border
      size="medium"
      style="width: 98%; margin-top:5px"
      @selection-change="handleSelectionChange"
      v-loading="loading"
      class="card-shadow"
    >
      <el-table-column type="selection" width="40"> </el-table-column>
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
      <el-table-column prop="fcontent" label="测试用例" min-width="800">
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
        v-if="qahead.fstatus !== '1'"
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
          <el-dropdown trigger="click" @command="handleResult">
            <el-tag :type="handleTag(scope.row.fresult)">{{
              scope.row.fresult
            }}</el-tag>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                :disabled="!isCanTest()"
                :command="beforeHandleResult('OK', scope.row)"
                >OK</el-dropdown-item
              >
              <el-dropdown-item
                :disabled="!isCanTest()"
                :command="beforeHandleResult('NG', scope.row)"
                >NG</el-dropdown-item
              >
              <el-dropdown-item
                :disabled="!isCanTest()"
                :command="beforeHandleResult('NGOK', scope.row)"
                >NGOK</el-dropdown-item
              >
              <el-dropdown-item
                :command="beforeHandleResult('CANCEL', scope.row)"
                :disabled="!isCanTest()"
                >CANCEL</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column label="贴图" width="100" >
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            style="margin-left:15px"
            @click="handleContentText(scope.row.id)"
            v-if="isCanImage(scope.row.test_tag)"
            >{{ scope.row.test_tag }}</el-link
          >
          <!-- <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            @click="handleContentText(scope.row.id)"
            v-show="!scope.row.fcontent_text && isCanTest()"
            >贴图</el-link
          > -->
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
            @click="singleModify(scope.row.id)"
            v-show="isCanEdit(scope.row)"
            style="margin-left:15px"
          ></el-link>
          <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            v-show="isCanEdit(scope.row)"
            @click="singleDelete(scope.row.id)"
            icon="el-icon-delete"
          ></el-link>
        </template>
      </el-table-column>
    </el-table>
    <SingleNewQaList
      ref="SingleNewQaList"
      :id="qahead.id"
      @refreshQaList="refreshQaList"
    ></SingleNewQaList>

    <BatchNewQaList
      ref="BatchNewQaList"
      :id="qahead.id"
      @refreshQaList="refreshQaList"
    ></BatchNewQaList>

    <QaModifyDetail
      ref="QaModifyDetail"
      @refreshTargetActual="refreshTargetActual"
    ></QaModifyDetail>

    <SingleModifyQaList
      ref="SingleModifyQaList"
      @refreshQaList="refreshQaList"
    ></SingleModifyQaList>

    <el-backtop target=".goTop" :bottom="100">
      <i class="el-icon-caret-top"></i>
    </el-backtop>
  </div>
</template>

<script>
import {
  getQaHead,
  getQaDetailByQaHead,
  deleteQaDetail,
  updateQaDetailResult,
  updateQaHead,
  putDefaultOK,
} from "./../../../services/qaService";
import SingleNewQaList from "../components/SingleNewQaList";
import BatchNewQaList from "../components/BatchNewQaList";
import SingleModifyQaList from "../components/SingleModifyQaList";
import QaModifyDetail from "../components/QaModifyDetail";
import MCLTargetActual from "../components/MCLTargetActual";
export default {
  components: {
    SingleNewQaList,
    SingleModifyQaList,
    BatchNewQaList,
    QaModifyDetail,
    MCLTargetActual,
  },
  data() {
    return {
      loading: false,
      paramtype: "",
      parentroute: "",
      fullscreenLoading: false,
      regressionTag: "",
      approvalTag: "",
      qahead: {},
      qadetails: [],
      multipleSelection: [],
    };
  },

  methods: {
    isCanEdit(row) {
      if (row.fapproval === "已审核") {
        return false;
      } else {
        if (row.fcontent_text || row.fresult) {
          return false;
        }
      }
      return true;
    },

    isCanDefaultOK() {
      if (this.qahead.fstatus === "2") {
        return true;
      } else {
        return false;
      }
    },

    isCanAdd() {
      if (this.qahead.fstatus === "1" || this.qahead.fstatus === "2") {
        return true;
      }
      return false;
    },

    isCanTest() {
      if (this.qahead.fstatus === "2") {
        return true;
      }
      return false;
    },

    isCanImage(test_tag){
      if (this.qahead.fstatus === "2") {
        return true
      }else{
        if(test_tag === '贴图'){
          return false;
        }
        return true;
      }
    },

    isCanRoback() {
      if (this.qahead.fstatus === "3") {
        return true;
      }
      return false;
    },

    isCanBatchDelete() {
      if ((this.qahead.fstatus === "1") & (this.qadetails.length > 0)) {
        return false;
      }
      return true;
    },

    isCanSubmit() {
      if (
        this.qahead.fstatus === "3" ||
        this.qahead.fstatus === "4" ||
        this.qahead.fstatus === "1"
      ) {
        return false;
      }

      for (var i in this.qadetails) {
        if (!this.qadetails[i].fresult) {
          return false;
        }
        if (this.qadetails[i].fresult === "NG") {
          return false;
        }
      }

      return true;
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

    beforeHandleResult(item, row) {
      return {
        command: item,
        row: row,
      };
    },

    handleContentText(id) {
      this.$router.push({
        name: "QaContentText",
        query: { type: "test", qadf_id: id },
      });
    },

    async batchDeleteQaDetail() {
      this.$confirm("此操作将永久删除选中的数据, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            this.fullscreenLoading = true;
            var selectData = this.$refs.multipleTable.selection;
            if (selectData.length > 0) {
              for (var i in selectData) {
                var resp = await deleteQaDetail(selectData[i].id).catch(() => {
                  this.$message.error("测试项删除异常");
                  this.fullscreenLoading = false;
                });
                if (
                  Object.prototype.hasOwnProperty.call(resp.data, "message")
                ) {
                  this.$message.error(resp.data.message);
                  this.fullscreenLoading = false;
                }
              }
              this.refreshQaList();
              this.$message({
                message: "批量删除成功！",
                type: "success",
              });
            }
            this.fullscreenLoading = false;
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },

    async resultSubmit() {
      this.qahead.fstatus = "3";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("测试结果提交异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
        this.qahead.fstatus = "2";
        return;
      } else {
        this.$message.success("测试结果提交成功");
      }
    },

    async resultRollback() {
      this.qahead.fstatus = "2";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("测试结果撤回异常");
      });
      console.log(resp);
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("测试结果撤回成功");
      }
    },

    async handleResult(command) {
      var qadetailInfo = {};

      qadetailInfo["id"] = command.row.id;
      qadetailInfo["fresult"] = command.command;

      var orig_result = command.row.fresult;
      var new_result = command.command;

      if (
        (orig_result === "NG" || orig_result === "CANCEL") &&
        new_result === "OK"
      ) {
        var info_message =
          "测试结果由 " +
          orig_result +
          " 修改到 " +
          new_result +
          " 不符合规定，是否继续?";
        this.$confirm(info_message, "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.updateResult(command.row.id, qadetailInfo);
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "取消操作",
            });
          });
      } else {
        this.updateResult(command.row.id, qadetailInfo);
      }
    },

    async updateResult(qadetail_id, qadetailInfo) {
      var resp = await updateQaDetailResult(qadetail_id, qadetailInfo).catch(
        () => {
          this.$message.error("测试项测试结果更新异常");
        }
      );
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("测试项更新成功");
        this.refreshQaList();
        this.refreshTargetActual();
      }
    },

    filterResult(value, row) {
      return row.fresult === value;
    },

    refreshTargetActual() {
      this.$refs.MCLTargetActual.refreshTargetActual();
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
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    singleAdd() {
      this.$refs.SingleNewQaList.handleDialog(this.qahead.id);
    },

    batchAdd() {
      this.$refs.BatchNewQaList.handleDialog(this.qahead.id);
    },

    singleModify(id) {
      this.$refs.SingleModifyQaList.handleDialog(id);
    },

    detailModify() {
      this.$refs.QaModifyDetail.handleDialog(this.qahead.id);
    },

    async singleDelete(id) {
      var resp = await deleteQaDetail(id).catch(() => {
        this.$message.error("测试项删除异常");
      });
      if (resp.status === 204) {
        this.refreshQaList();
        this.$message({
          message: "删除成功！",
          type: "success",
        });
      }
    },

    async defaultOK() {
      var resp = await putDefaultOK(this.qahead.id).catch(() => {
        this.$message.error("Default OK数据异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
        return;
      }
      this.refreshQaList();
    },
  },
  mounted: async function() {
    this.loading = true;
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

    // this.bus.$on("refreshList", function() {
    //   this.refreshQaList();
    // });
    this.loading = false;
  },
};
</script>

<style>
.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
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
