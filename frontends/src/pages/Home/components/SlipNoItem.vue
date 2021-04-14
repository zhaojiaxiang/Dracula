<template>
  <div class="div-style-1">
    <el-table :data="tableData" style="width: 100%" size="medium">
      <el-table-column
        prop="fstatus"
        label="状态"
        fixed
        width="80"
        :filters="[
          { text: '待办', value: '待办' },
          { text: '进行中', value: '进行中' },
          { text: '已完成', value: '已完成' },
          { text: '已发布', value: '已发布' },
        ]"
        :filter-method="filterStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-dropdown trigger="click" @command="handleStatus">
            <el-tag :class="statusTagClass(scope.row.fstatus)" disable-transitions effect="plain">{{
              scope.row.fstatus
            }}</el-tag>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                v-show="
                  true
                    ? scope.row.fstatus != '待办'
                    : scope.row.fstatus == '待办'
                "
                :command="beforeHandleStatus('1', scope.row)"
                >待办</el-dropdown-item
              >
              <el-dropdown-item
                v-show="
                  true
                    ? scope.row.fstatus != '进行中'
                    : scope.row.fstatus == '进行中'
                "
                :command="beforeHandleStatus('2', scope.row)"
                >开始</el-dropdown-item
              >
              <el-dropdown-item
                v-show="
                  true
                    ? scope.row.fstatus != '已完成'
                    : scope.row.fstatus == '已完成'
                "
                :command="beforeHandleStatus('3', scope.row)"
                >完成</el-dropdown-item
              >
              <el-dropdown-item
                v-show="
                  true
                    ? scope.row.fstatus != '已发布'
                    : scope.row.fstatus == '已发布'
                "
                :command="beforeHandleStatus('4', scope.row)"
                >发布</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column
        fixed
        prop="ftype"
        label="类型"
        width="100"
        :filters="[
          { text: '追加开发', value: '追加开发' },
          { text: '改善需求', value: '改善需求' },
          { text: '维护阶段障碍', value: '维护阶段障碍' },
        ]"
        :filter-method="filterType"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="typeTagClass(scope.row.ftype)" disable-transitions>{{
            scope.row.ftype
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed prop="fslipno" label="联络票号" min-width="160">
        <template slot-scope="scope">
          <el-link
            @click="openSlipNoQa(scope.row.fslipno, scope.row.fstatus)"
            type="primary"
            :underline="false"
            >{{ scope.row.fslipno }}</el-link
          >
        </template>
      </el-table-column>
      <el-table-column prop="fodrno" label="订单号" min-width="100">
      </el-table-column>
      <el-table-column prop="fbrief" label="详情" min-width="370" show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="plan" label="计划" width="220"> </el-table-column>
      <el-table-column prop="actual" label="实际" width="220">
      </el-table-column>
      <el-table-column prop="freleasedt" label="发布" width="110">
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="120">
        <template slot-scope="scope">
          <el-link
            @click="openSlipNoModifiy(scope.row.id)"
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
          ></el-link>
          <el-link
            style="margin-left:40px"
            @click="deleteInitLiaison(scope.row.id, scope.row.fslipno)"
            type="primary"
            v-show="
              true ? scope.row.fstatus == '待办' : scope.row.fstatus != '待办'
            "
            :underline="false"
            icon="el-icon-delete"
          ></el-link>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <el-pagination
        background
        layout="prev, pager, next"
        :hide-on-single-page="true"
        :total="liaisonTotal"
        :page-size="pageSize"
        :current-page="currentPage"
        :page-count="pageCount"
        @current-change="handlePage"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import {
  getLiaisonsViaPagination,
  updateLiaisonStatus,
  getSingleLiaison,
  deleteLiaison,
} from "../../../services/liaisonService";
export default {
  data() {
    return {
      currentPage: 1,
      liaisonTotal: 0,
      pageSize: 10,
      pageCount:1,
      currentID: 0,
      tableData: [],
    };
  },
  methods: {
    handlePage(page) {
      this.currentPage = page;
      this.refreshLiaisons();
    },

    openSlipNoModifiy(id) {
      this.bus.$emit("openSlipNoModifiy", id);
    },
    openSlipNoQa(fslipno, fstatus) {
      if (fstatus !== "待办"){
        this.$router.push({ path: "/qa/", query: { slipno: fslipno } });
      }else{
        this.$message.error("请先开始该项目");
      }
    },

    typeTagClass(type){
      if(type === "追加开发"){
        return "success"
      }else if(type === "改善需求"){
        return "warning"
      }else{
        return "danger"
      }
    },

    statusTagClass(status){
      if(status === "待办"){
        return "status-1"
      }else if(status === "进行中"){
        return "status-2"
      }else if(status === "已完成"){
        return "status-3"
      }else{
        return "status-4"
      }
    },

    filterStatus(value, row) {
      console.log('fileter')
      return row.fstatus === value;
    },
    filterType(value, row) {
      return row.ftype === value;
    },

    calcPageTotal(liaisonCount, pageSize) {
      liaisonCount = this.liaisonTotal
      pageSize = this.pageSize
      var remainder = liaisonCount % pageSize;
      if (remainder === 0) {
        this.pageCount = liaisonCount / pageSize;
      } else {
        this.pageCount = parseInt(liaisonCount / pageSize) + 1;
      }
    },

    async refreshLiaisons() {
      this.tableData = [];
      // var resp = await getLiaisons();
      var resp = await getLiaisonsViaPagination(
        this.currentPage,
        this.pageSize
      ).catch(()=>{
        this.$message.error("联络票数据获取异常")
        return
      });

      var liaisons = [];
     
      this.liaisonTotal = resp.data.count
      this.calcPageTotal();
      liaisons = resp.data.results;
      
      for (var i in liaisons) {
        var id = liaisons[i].id;
        var ftype = liaisons[i].ftype;
        var fstatus = liaisons[i].fstatus;
        var fslipno = liaisons[i].fslipno;
        var fbrief = liaisons[i].fbrief;
        var fplnstart = liaisons[i].fplnstart;
        var fplnend = liaisons[i].fplnend;
        var factstart = liaisons[i].factstart;
        var factend = liaisons[i].factend;
        var freleasedt = liaisons[i].freleasedt;
        var fodrno = liaisons[i].fodrno;

        var plan = fplnstart + " ~ " + fplnend;
        var actual = "";

        if (fstatus === "1") {
          fstatus = "待办";
        } else if (fstatus === "2") {
          fstatus = "进行中";
          actual = factstart;
        } else if (fstatus === "3") {
          fstatus = "已完成";
          actual = factstart + " ~ " + factend;
        } else if (fstatus === "4") {
          fstatus = "已发布";
          actual = factstart + " ~ " + factend;
        }

        var liaison = {
          id: id,
          ftype: ftype,
          fstatus: fstatus,
          fslipno: fslipno,
          fbrief: fbrief,
          plan: plan,
          actual: actual,
          freleasedt: freleasedt,
          fodrno: fodrno
        };
        this.tableData.push(liaison);
      }
    },

    async handleStatus(command) {
      var get_resp = await getSingleLiaison(command.row.id).catch(()=>{
        this.$message.error("联络票数据获取异常")
        return
      });
      if (get_resp.status === 200) {
        var liaison = get_resp.data;
        var status = command.command;
        if (status == "3" && Number(liaison.factmanpower) == 0) {
          this.$message.error("请先填写实际工数");
          return;
        }
        if (status === liaison.fstatus) {
          return;
        }
        var statusInfo = {
          fslipno: liaison.fslipno,
          fodrno: liaison.fodrno,
          fstatus: status,
        };
        var put_resp = await updateLiaisonStatus(
          command.row.id,
          statusInfo
        ).catch(() => {
          this.$message.error("联络票号数据更新异常");
        });

        if(Object.prototype.hasOwnProperty.call(put_resp.data, "message")){
          this.$message.error(put_resp.data.message);
          return
        }else{
          this.$emit("refreshHome");
          this.$message({
            message: statusInfo.fslipno + "状态更新成功！",
            type: "success",
          });
        }
      } else {
        this.$message.error("联络票号数据获取异常");
      }
    },
    beforeHandleStatus(item, row) {
      return {
        command: item,
        row: row,
      };
    },
    deleteInitLiaison(id, slipno) {
      this.$confirm("此操作将永久删除" + slipno + ", 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            var resp = await deleteLiaison(id).catch(()=>{
              this.$message.error("联络票删除异常")
            });
            if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
              this.$emit("refreshHome");
              this.$message({
                message: slipno + "已经删除！",
                type: "success",
              });
              for (var i in this.tableData) {
                if (this.tableData[i].id === id) {
                  this.tableData.splice(i, 1);
                }
              }
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
  },
  mounted: function() {
    this.refreshLiaisons();
  },
};
</script>

<style>
.status-1{
  background-color: #fbe6d4;
  border-color: #fbe6d4;
  color: #ffa931;
}
.status-2{
  background-color: #fecb89;
  border-color: #fecb89;
  color: #fff;
}
.status-3{
  background-color: #ffa931;
  color: #fff;
  border-color: #ffa931;
}
.status-4{
  background-color: #b9ac92;
  border-color: #b9ac92;
  color: #fff;
}

.el-table--medium td,
.el-table--medium th {
  padding: 5px 0px;
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
.div-style-1 {
  margin: 0px;
  box-shadow:4px 4px 40px rgba(0,0,0,.05)
}
</style>
