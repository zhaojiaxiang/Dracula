<template>
  <div>
    <el-breadcrumb
      separator-class="el-icon-arrow-right"
      style="font-size:16px;margin-top: 5px;"
    >
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>任务列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-table
      :data="tasktable"
      border
      style="width:98%;margin-top:20px"
      size="medium"
      v-loading="loading"
    >
      <el-table-column prop="ftesttyp" label="测试类型" width="80">
      </el-table-column>
      <el-table-column prop="fodrno" label="订单号" width="100">
      </el-table-column>

      <el-table-column
        prop="fslipno"
        label="联络票/订单支号"
        width="200"
      >
      </el-table-column>

      <el-table-column
        prop="fobjectid"
        label="测试对象"
        width="250"
        show-overflow-tooltip
      >
      </el-table-column>

      <el-table-column
        prop="fobjmodification"
        label="概要"
        show-overflow-tooltip
      >
      </el-table-column>

      <el-table-column label="设计Review" width="110">
        <template slot-scope="scope">
          <el-link
            @click="handleClick(scope.row)"
            style="margin-left:10px"
            type="text"
            size="medium"
            v-show="scope.row.design_id"
            :underline="false"
            >设计Review</el-link
          >
        </template>
      </el-table-column>

      <el-table-column label="代码Review" width="110">
        <template slot-scope="scope">
          <el-link
            @click="handleClick(scope.row)"
            style="margin-left:10px"
            type="text"
            size="medium"
            v-show="scope.row.code_id"
            :underline="false"
            >代码Review</el-link
          >
        </template>
      </el-table-column>

      <el-table-column label="操作" width="120">
        <template slot-scope="scope">
          <el-link
            style="margin-left:10px"
            type="text"
            size="medium"
            :underline="false"
            v-show="paramtype === 'mcl' || paramtype === 'pcl'"
            @click="openQaTestList(scope.row.qahf_id, paramtype)"
            >测试</el-link
          >

          <el-link
            style="margin-left:10px"
            type="text"
            size="medium"
            :underline="false"
            v-show="paramtype === 'approval'"
            @click="openMyTaskList(scope.row.qahf_id, paramtype)"
            >审核</el-link
          >

          <el-link
            style="margin-left:10px"
            type="text"
            size="medium"
            :underline="false"
            v-show="paramtype === 'confirm'"
            @click="openMyTaskList(scope.row.qahf_id, paramtype)"
            >确认</el-link
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {
  getMyMCL,
  getMyPCL,
  getMyConfirm,
  getMyApproval,
  getMyRelease,
} from "./../../../services/liaisonService";
export default {
  data() {
    return {
      loading: false,
      paramtype: "",
      tasktable: [],
    };
  },
  methods: {
    openQaTestList(id, paramtype) {
      var routername;
      if (paramtype === "mcl") {
        routername = "QaTestList";
      } else {
        routername = "QaPclList";
      }
      this.$router.push({
        name: routername,
        query: { qahf_id: id, type: paramtype },
      });
    },

    openMyTaskList(id, paramtype) {
      this.$router.push({
        name: "TaskList",
        query: { qahf_id: id, type: paramtype },
      });
    },

    async refreshTask() {
      this.paramtype = this.$route.query.type;
      var resp;
      if (this.paramtype === "release") {
        resp = await getMyRelease().catch(() => {
          this.$message.error("待审核数据获取异常");
        });
        this.tasktable = resp.data;
      } else {
        if (this.paramtype === "mcl") {
          resp = await getMyMCL().catch(() => {
            this.$message.error("单体测试数据获取异常");
          });
          this.tasktable = resp.data;
        }
        if (this.paramtype === "pcl") {
          resp = await getMyPCL().catch(() => {
            this.$message.error("单体测试数据获取异常");
          });
          this.tasktable = resp.data;
        }
        if (this.paramtype === "approval") {
          resp = await getMyApproval().catch(() => {
            this.$message.error("待审核数据获取异常");
          });
          this.tasktable = resp.data;
        }
        if (this.paramtype === "confirm") {
          resp = await getMyConfirm().catch(() => {
            this.$message.error("待确认数据获取异常");
          });
          this.tasktable = resp.data;
        }
      }
    },
  },
  mounted: function() {
    this.loading = true;
    this.refreshTask();
    this.loading = false;
  },
};
</script>

<style></style>
