<template>
  <div style="margin:0 auto">
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <el-row>
      <el-col :span="3">
        <div class="grid-content"></div>
      </el-col>
      <el-col :span="17"
        ><div style="margin-top:30px">
          <el-button @click="openOrderInfo" plain>查看所有项</el-button>
          <el-button :disabled="multipleslip.length === 0" @click="openPartOrderInfo" plain>查看选择项</el-button>
          <el-table
            ref="multipleTable"
            :data="tableData"
            tooltip-effect="dark"
            style="width: 100%; margin-top:10px"
            border
            stripe
            size="medium"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" :selectable="selecttable"> </el-table-column>
            <el-table-column prop="fsystemcd" label="系统名称" width="120">
            </el-table-column>
            <el-table-column prop="fslipno" label="联络票号" width="250">
            </el-table-column>
            <el-table-column prop="fsirno" label="Sir号" width="150">
            </el-table-column>
            <el-table-column
              prop="fbrief"
              label="开发概要"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column fixed="right" label="查看单个报表" width="150">
              <template slot-scope="scope">
                <el-link
                  @click="openQaList(scope.row.fslipno)"
                  type="primary"
                  :underline="false"
                  icon="el-icon-tickets"
                ></el-link>
              </template>
            </el-table-column>
          </el-table></div
      ></el-col>
    </el-row>
  </div>
</template>

<script>
import { getReportList, getReportPCLList } from "../../services/report";
export default {
  data() {
    return {
      order_no:"",
      tableData: [],
      multipleslip: "",
    };
  },
  methods: {
    goBack() {
      //返回上一个路由
      this.$router.go(-1)
    },

    selecttable(row) {
      if (row.fsystemcd === "PCL") {
        return false;
      } else {
        return true;
      }
    },

    handleSelectionChange(val) {
      var slip_arr = []
      val.forEach(element => {
        slip_arr.push(element.fslipno)
      });
      this.multipleslip = slip_arr.join(",")
    },

    openQaList(slipno) {
      this.$router.push({ name: "ReportSingle", query: { slipno: slipno } });
    },

    openOrderInfo(){
      this.$router.push({ name: "ReportMultiple", query: { order_no: this.order_no } });
    },

    openPartOrderInfo(){
      this.$router.push({ name: "ReportMultiple", query: { order_no: this.order_no, multiple_slip:this.multipleslip } });
    },

  },
  mounted: async function() {
    this.order_no = this.$route.query.order_no;
    var resp = await getReportList(this.order_no).catch(() => {
      this.$message.error("报表列表数据获取异常");
    });
    this.tableData = resp.data;

    var resp_pcl = await getReportPCLList(this.order_no).catch(() => {
      this.$message.error("报表PCL列表数据获取异常");
    });

    // this.tableData = resp.data + resp_pcl.data;

    if(resp_pcl.data){
      resp_pcl.data.forEach(element => {
        this.tableData.push(element)
      });
    }
    
  },
};
</script>

<style>
.bg-purple {
  background: #d3dce6;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
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
</style>
