<template>
  <div class="goTop">
    <el-row>
      <el-col :span="15"
        ><div>
          <el-breadcrumb
            separator-class="el-icon-arrow-right"
            style="font-size:16px;margin-top: 5px;"
          >
            <el-breadcrumb-item
              :to="{
                name: 'ProjectOverview',
                query: { order_no: this.qahead.fslipno },
              }"
              >订单概览</el-breadcrumb-item
            >
            <el-breadcrumb-item
              :to="{
                name: 'ProjectPclClass1',
                query: { qahf_id: this.qahead.id },
              }"
              >PCL列表 -- {{ this.qahead.fobjectid }}</el-breadcrumb-item
            >
            <el-breadcrumb-item
              :to="{
                name: 'ProjectPclClass2',
                query: { qahf_id: this.qahead.id, class1: this.class1 },
              }"
              >{{ this.class1 }}</el-breadcrumb-item
            >
            <el-breadcrumb-item>{{ this.class2 }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div></el-col
      >
      <el-col :span="9">
        <div>
          <PCLTargetActual></PCLTargetActual>
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
            <el-button v-show="isCanAdd()" @click="singleAdd()"
              >逐条添加</el-button
            >
            <el-button v-show="isCanAdd()" @click="batchAdd()"
              >批量添加</el-button
            >
            <el-button
              type="primary"
              v-show="isCanSubmit"
              @click="resultSubmit()"
              >提交结果</el-button
            >
            <el-button v-show="isCanRollback" @click="resultRollback()"
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
    >
      <el-table-column type="selection" width="40"> </el-table-column>
      <el-table-column label="序号" type="index" width="50"> </el-table-column>
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
      <el-table-column label="贴图" width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            style="margin-left:15px"
            @click="handleContentText(scope.row.id)"
            v-show="scope.row.fcontent_text"
            >{{ scope.row.test_tag }}</el-link
          >
          <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            @click="handleContentText(scope.row.id)"
            v-show="!scope.row.fcontent_text && isCanTest()"
            >贴图</el-link
          >
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
    <SingleNewQaListforPCL
      ref="SingleNewQaListforPCL"
      :id="qahead.id"
      @refreshQaList="refreshQaList"
    ></SingleNewQaListforPCL>

    <BatchNewPclList
      ref="BatchNewPclList"
      :id="qahead.id"
      @refreshQaList="refreshQaList"
    ></BatchNewPclList>

    <SingleModifyQaListforPCL
      ref="SingleModifyQaListforPCL"
      @refreshQaList="refreshQaList"
    ></SingleModifyQaListforPCL>

    <el-backtop target=".goTop" :bottom="100">
      <i class="el-icon-caret-top"></i>
    </el-backtop>
  </div>
</template>

<script>
import {
  getQaHead,
  getPCLDetailbyClass,
  deleteQaDetail,
  updateQaDetailResult,
  getPCLCommitJudgment,
  updateQaHead,
} from "./../../../services/qaService";
import SingleNewQaListforPCL from "../../Home/components/SingleNewQaListforPCL";
import BatchNewPclList from "../../Home/components/BatchNewPclList";
import SingleModifyQaListforPCL from "../../Home/components/SingleModifyQaListforPCL";
import PCLTargetActual from "../../Home/components/PCLTargetActual";
export default {
  components: {
    SingleNewQaListforPCL,
    SingleModifyQaListforPCL,
    BatchNewPclList,
    PCLTargetActual,
  },
  data() {
    return {
      loading: false,
      paramtype: "",
      fullscreenLoading: false,
      approvalTag: "",
      class1: "",
      class2: "",
      isCanSubmit: false,
      isCanRollback: false,
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

    isCanBatchDelete() {
      if (this.qahead.fstatus === "1") {
        return false;
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
                });
                if (
                  Object.prototype.hasOwnProperty.call(resp.data, "message")
                ) {
                  this.$message.error(resp.data.message);
                }
              }
              this.refreshQaList();
              this.fullscreenLoading = false;
              this.$message({
                message: "批量删除成功！",
                type: "success",
              });
            }
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
      } else {
        this.$message.success("测试结果提交成功");
      }
      this.refreshQaList();
    },

    async resultRollback() {
      this.qahead.fstatus = "2";
      var resp = await updateQaHead(this.qahead.id, this.qahead).catch(() => {
        this.$message.error("测试结果撤回异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("测试结果撤回成功");
      }
      this.refreshQaList();
    },

    async handleResult(command) {
      var qadetailInfo = {};

      qadetailInfo["id"] = command.row.id;
      qadetailInfo["fresult"] = command.command;

      var resp = await updateQaDetailResult(command.row.id, qadetailInfo).catch(
        () => {
          this.$message.error("测试项测试结果更新异常");
        }
      );

      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("测试项更新成功");
      }

      var newqadetail = this.qadetails;
      for (var i in newqadetail) {
        if (newqadetail[i].id === command.row.id) {
          newqadetail[i] = command.command;
        }
      }
      // this.qadetails = []
      // this.qadetails = newqadetail
      this.refreshQaList();
    },

    filterResult(value, row) {
      return row.fresult === value;
    },

    async refreshQaList() {
      var resp = await getPCLDetailbyClass(
        this.qahead.id,
        this.class1,
        this.class2
      ).catch(() => {
        this.$message.error("测试项数据获取异常");
      });
      if (resp.status === 200) {
        var qadata = resp.data;
        console.log(resp);
        for (var i in qadata) {
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

      var resp_pcl = await getPCLCommitJudgment(this.qahead.id).catch(() => {
        this.$message.error("PCL结果数据获取异常");
      });

      if (resp_pcl.status === 200) {
        var pcl = resp_pcl.data;
        if ((pcl.status === "2") & (pcl.result === "OK")) {
          this.isCanSubmit = true;
        } else {
          this.isCanSubmit = false;
        }
        if (pcl.status === "3") {
          this.isCanRollback = true;
        } else {
          this.isCanRollback = false;
        }
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    singleAdd() {
      this.$refs.SingleNewQaListforPCL.handleDialog(this.qahead.id);
    },

    batchAdd() {
      this.$refs.BatchNewPclList.handleDialog(this.qahead.id);
    },

    singleModify(id) {
      this.$refs.SingleModifyQaListforPCL.handleDialog(id);
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
  },
  mounted: async function() {
    this.loading = true;
    var id = this.$route.query.qahf_id;
    this.class1 = this.$route.query.class1;
    this.class2 = this.$route.query.class2;
    this.paramtype = this.$route.query.type;
    var resp = await getQaHead(id).catch(() => {
      this.$message.error("测试对象数据获取异常");
    });
    if (resp.status === 200) {
      this.qahead = resp.data;
      this.refreshQaList();
    }

    this.bus.$on("refreshList", function() {
      this.refreshQaList();
    });
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
