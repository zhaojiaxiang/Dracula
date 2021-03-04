<template>
  <div class="goTop">
    <el-breadcrumb
      separator-class="el-icon-arrow-right"
      style="font-size:16px;margin-top: 5px;"
    >
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item
        v-show="paramtype !== 'pcl'"
        :to="{ path: '/qa/', query: { slipno: this.qahead.fslipno } }"
        >QA列表</el-breadcrumb-item
      >
      <el-breadcrumb-item
        v-show="paramtype === 'pcl'"
        :to="{ path: '/task/', query: { type: this.paramtype } }"
        >任务列表</el-breadcrumb-item
      >
      <el-breadcrumb-item
        >PCL列表 -- {{ this.qahead.fobjectid }}</el-breadcrumb-item
      >
    </el-breadcrumb>

    <el-row style="margin-top:20px">
      <el-col :span="12">
        <div>
          <el-button
            type="danger"
            v-loading.fullscreen.lock="fullscreenLoading"
            @click="batchDeleteQaDetail()"
            :disabled="isCanDelete"
            >删除选中项</el-button
          >
        </div>
      </el-col>
      <el-col :span="12">
        <div style="text-align:right;margin-right:40px">
          <el-button-group>
            <el-button @click="singleAdd()">逐条添加</el-button>
            <el-button @click="batchAdd()">批量添加</el-button>
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
      <el-table-column
        prop="fclass1"
        label="分类1"
        width="100"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <el-link
            @click="openClass2(scope.row.fclass1)"
            type="primary"
            :underline="false"
            >{{ scope.row.fclass1 }}</el-link
          >
        </template>
      </el-table-column>
      <el-table-column prop="class2_cnt" label="分类2数量" width="150">
      </el-table-column>
      <el-table-column prop="test_cnt" label="测试用例数量" width="150">
      </el-table-column>
      <el-table-column prop="tested_cnt" label="已经测试数量" width="150">
      </el-table-column>
      <el-table-column prop="ng" label="未处理NG数量" width="150">
      </el-table-column>
      <el-table-column prop="canceled_cnt" label="取消数量" width="150">
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
  deleteQaDetail,
  getQaDetailByQaHeadandClass1,
  updateQaDetailResult,
  updateQaHead,
  getPclQaClass1,
  getPCLCommitJudgment,
} from "./../../../services/qaService";
import SingleNewQaListforPCL from "../components/SingleNewQaListforPCL";
import BatchNewPclList from "../components/BatchNewPclList";
import SingleModifyQaListforPCL from "../components/SingleModifyQaListforPCL";
export default {
  components: {
    SingleNewQaListforPCL,
    SingleModifyQaListforPCL,
    BatchNewPclList,
  },
  data() {
    return {
      loading: false,
      paramtype: "",
      parentroute: "",
      fullscreenLoading: false,
      regressionTag: "",
      approvalTag: "",
      isCanSubmit: false,
      isCanRollback: false,
      isCanDelete: true,
      qahead: {},
      qadetails: [],
      multipleSelection: [],
    };
  },

  methods: {
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
            console.log(selectData);
            if (selectData.length > 0) {
              for (var i in selectData) {
                var resp_head = await getQaDetailByQaHeadandClass1(
                  this.qahead.id,
                  selectData[i].fclass1
                ).catch(() => {
                  this.$message.error("测试项获取异常");
                });

                if (
                  Object.prototype.hasOwnProperty.call(resp_head.data, "message")
                ) {
                  this.$message.error(resp.data.message);
                }

                for (var j in resp_head.data) {
                  var qadf = resp_head.data[j].id;
                  var resp = await deleteQaDetail(qadf).catch(() => {
                    this.$message.error("测试项删除异常");
                  });
                  if (
                    Object.prototype.hasOwnProperty.call(resp.data, "message")
                  ) {
                    this.$message.error(resp.data.message);
                  }
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

    openClass2(class1) {
      this.$router.push({
        name: "QaPclClass2",
        query: {
          qahf_id: this.qahead.id,
          type: this.paramtype,
          class1: class1,
        },
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

      this.refreshQaList();
    },

    filterResult(value, row) {
      return row.fresult === value;
    },

    async refreshQaList() {
      var resp = await getPclQaClass1(this.qahead.id).catch(() => {
        this.$message.error("测试项数据获取异常");
      });
      if (resp.status === 200) {
        this.qadetails = resp.data.class1;
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
        if (pcl.status === "1") {
          this.isCanDelete = false;
        } else {
          this.isCanDelete = true;
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
