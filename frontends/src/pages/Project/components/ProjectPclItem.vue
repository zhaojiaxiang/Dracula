<template>
  <div>
    <el-row style="margin-top:20px; margin-bottom:5px">
      <el-col :span="12">
        <Guide>
          <template>
            <div>
              <h5><strong>结合测试</strong></h5>
            </div>
          </template>
        </Guide>
      </el-col>

      <el-col :span="12">
        <div style="text-align:right;">
          <el-button v-show="isCanAddPCL" @click="openPCLNew"
            >新建结合测试</el-button
          >
        </div>
      </el-col>
    </el-row>
    <el-table :data="pcltable" border size="medium" v-loading="loading">
      <el-table-column prop="fslipno" label="订单号" width="200">
      </el-table-column>

      <el-table-column prop="fslipno2" label="订单支号" width="100">
      </el-table-column>

      <el-table-column
        prop="fstatus"
        label="状态"
        width="100"
        :filters="[
          { text: '初始', value: '初始' },
          { text: '已审核', value: '已审核' },
          { text: '已提交', value: '已提交' },
          { text: '已确认', value: '已确认' },
        ]"
        :filter-method="filterStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.tagtype" disable-transitions>{{
            scope.row.fstatus
          }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="fobjectid" label="测试对象" width="200">
      </el-table-column>

      <el-table-column prop="fcreateusr" label="创建者" width="100">
      </el-table-column>

      <el-table-column prop="ftestusr" label="测试者" width="100">
      </el-table-column>

      <el-table-column prop="qadfcount" label="测试项数量" width="100">
      </el-table-column>

      <el-table-column label="操作" width="80">
        <template slot-scope="scope">
          <el-link
            @click="openPclModify(scope.row.id)"
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
            v-show="scope.row.qadfcount === 0"
          ></el-link>
          <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            v-show="scope.row.qadfcount === 0"
            @click="deleteQaHead(scope.row.id, scope.row.fobjectid)"
            icon="el-icon-delete"
          ></el-link>
        </template>
      </el-table-column>
      <el-table-column label="测试" width="80">
        <template slot-scope="scope">
          <el-link
            style="margin-left:10px"
            type="text"
            size="medium"
            :underline="false"
            @click="openQaTestList(scope.row.id)"
            >测试</el-link
          >
        </template>
      </el-table-column>
    </el-table>
    <ProjectPclNew
      ref="ProjectPclNew"
      @refreshPCLList="refreshPCLList"
    ></ProjectPclNew>

    <ProjectPclModify
      ref="ProjectPclModify"
      @refreshPCLList="refreshPCLList"
    ></ProjectPclModify>
  </div>
</template>

<script>
import { getQaHeadBySlipNo, deleteQaHead } from "./../../../services/qaService";
import { getQaProjectGroup } from "../../../services/projectService";
import ProjectPclNew from "./ProjectPclNew";
import ProjectPclModify from "./ProjectPclModify";
import Guide from "./../../Home/components/Guide";
export default {
  components: {
    ProjectPclNew,
    ProjectPclModify,
    Guide,
  },
  data() {
    return {
      loading: false,
      order_no: "",
      any_qahf_id: "",
      order_info: {},
      pcltable: [],
    };
  },
  methods: {
    openQaTestList(id) {
      this.$router.push({
        name: "ProjectPclClass1",
        query: { qahf_id: id },
      });
    },

    openPclModify(id) {
      this.$refs.ProjectPclModify.handleDialog(id);
    },

    openPCLNew() {
      this.$refs.ProjectPclNew.handleDialog(this.any_qahf_id);
    },

    isCanAddPCL() {
      if (this.order_info.status == 4) {
        return false;
      }
      return true;
    },

    deleteQaHead(id, fobjectid) {
      this.$confirm("此操作将永久删除" + fobjectid + ", 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            var resp = await deleteQaHead(id);
            if (resp.status == 204) {
              this.refreshPCL();
              this.$message({
                message: fobjectid + "已经删除！",
                type: "success",
              });
            } else {
              this.$message.error(resp.data.message);
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

    filterStatus(value, row) {
      return row.fstatus === value;
    },

    refreshPCLList() {
      console.log("re");
      this.refreshPCL();
    },

    async refreshPCL() {
      this.order_no = this.$route.query.order_no;

      var resp_order = await getQaProjectGroup(
        "",
        "",
        this.order_no,
        1,
        1
      ).catch(() => {
        this.$message.error("订单数据获取异常");
      });
      this.order_info = resp_order.data.results[0];

      var resp = await getQaHeadBySlipNo(this.order_no).catch(() => {
        this.$message.error("PCL信息获取异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      }
      this.pcltable = resp.data;

      if (this.pcltable.length > 0) {
        this.any_qahf_id = resp.data[0].id;

        for (var i in this.pcltable) {
          if (this.pcltable[i].fstatus === "1") {
            this.pcltable[i].fstatus = "初始";
            this.pcltable[i].tagtype = "info";
          } else if (this.pcltable[i].fstatus === "2") {
            this.pcltable[i].fstatus = "已审核";
            this.pcltable[i].tagtype = "";
          } else if (this.pcltable[i].fstatus === "3") {
            this.pcltable[i].fstatus = "已提交";
            this.pcltable[i].tagtype = "warning";
          } else if (this.pcltable[i].fstatus === "4") {
            this.pcltable[i].fstatus = "已确认";
            this.pcltable[i].tagtype = "success";
          }
        }
      }
    },
  },
  mounted: function() {
    this.loading = true;
    this.refreshPCL();
    this.loading = false;
  },
};
</script>

<style></style>
