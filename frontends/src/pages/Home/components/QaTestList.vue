<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right" style="font-size:16px">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item
        :to="{ path: '/qa/', query: { slipno: this.qahead.fslipno } }"
        >QA</el-breadcrumb-item
      >
      <el-breadcrumb-item>QA List</el-breadcrumb-item>
    </el-breadcrumb>

    <el-row style="margin-top:20px">
      <el-col :span="12">
        <div>
          <el-button type="danger" :disabled="qahead.fstatus !== '1'"
            >删除选中项</el-button
          >
        </div>
      </el-col>
      <el-col :span="12">
        <div style="text-align:right;margin-right:40px">
          <el-button @click="detailModify()">修改明细</el-button>
          <el-button @click="singleAdd()">逐条添加</el-button>
          <el-button @click="batchAdd()">批量添加</el-button>
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
      ></el-table-column>
      <el-table-column label="贴图" width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            style="margin-left:15px"
            v-show="scope.row.fcontent_text.length > 0"
            >已贴图</el-link
          >
          <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            v-show="scope.row.fcontent_text.length === 0"
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
    ></QaModifyDetail>

    <SingleModifyQaList
      ref="SingleModifyQaList"
      @refreshQaList="refreshQaList"
    ></SingleModifyQaList>
  </div>
</template>

<script>
import {
  getQaHead,
  getQaDetailByQaHead,
  deleteQaDetail,
} from "./../../../services/qaService";
import SingleNewQaList from "../components/SingleNewQaList";
import BatchNewQaList from "../components/BatchNewQaList";
import SingleModifyQaList from "../components/SingleModifyQaList";
import QaModifyDetail from "../components/QaModifyDetail";
export default {
  components: {
    SingleNewQaList,
    SingleModifyQaList,
    BatchNewQaList,
    QaModifyDetail,
  },
  data() {
    return {
      regressionTag:"",
      approvalTag:"",
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
        if (row.fcontent_text.length > 0) {
          return false;
        }
      }
      return true;
    },

    async refreshQaList() {
      var resp = await getQaDetailByQaHead(this.qahead.id).catch(()=>{
        this.$message.error("测试项数据获取异常")
      });
      if (resp.status === 200) {
        var qadata = resp.data;
        for(var i in qadata){
          if (qadata[i].fregression === "Y"){
            qadata[i].fregression = "是"
            this.regressionTag = ""
          }else{
            qadata[i].fregression = "否"
            this.regressionTag = "info"
          }
          if( qadata[i].fapproval === "Y"){
            qadata[i].fapproval = "已审核"
            this.approvalTag = ""
          }else{
            qadata[i].fapproval = "未审核"
            this.approvalTag = "info"
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
      var resp = await deleteQaDetail(id).catch(()=>{
        this.$$message.error("测试项删除异常")
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
    var id = this.$route.query.qahf_id;
    var resp = await getQaHead(id).catch(()=>{
      this.$message.error("测试对象数据获取异常")
    });
    if (resp.status === 200) {
      this.qahead = resp.data;
      this.refreshQaList();
    }
  },
};
</script>

<style>
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
