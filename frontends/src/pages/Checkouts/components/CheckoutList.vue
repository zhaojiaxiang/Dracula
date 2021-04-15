<template>
  <div class="div-style">
    <div style="text-align:center; margin-top:15px">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item>
          <el-select v-model="system" clearable placeholder="系统">
            <el-option
              v-for="item in systemList"
              :key="item.value"
              :label="item.value"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="chkstatus" clearable placeholder="状态">
            <el-option
              v-for="item in chkstatusList"
              :key="item.value"
              :label="item.value"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="applicant" clearable placeholder="申请人">
            <el-option
              v-for="(item, i) in groupusers"
              :key="i"
              :v-label="item.name"
              :value="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="chkoutobj"
            placeholder="迁出文件"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="slipno"
            placeholder="联络票号"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQuery">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQueryAll">查询全部</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-row style="margin-top:0px">
      <el-col :span="12">
        <div>
          <el-button type="danger" @click="batchDeleteCheckoutData"
            >删除选中项</el-button
          >
        </div>
      </el-col>
      <el-col :span="12">
        <div style="text-align:right;margin-right:10px">
          <el-button-group>
            <el-button @click="onWorkSpace">工作台</el-button>
            <el-button @click="openDialog('new', '')">新建</el-button>
            <el-button @click="openSendMail">邮件发送</el-button>
          </el-button-group>
        </div>
      </el-col>
    </el-row>
    <el-table
      ref="updateTable"
      :data="tableData"
      style="width:100%;margin-top:20px"
      size="medium"
      border
    >
      <el-table-column
        type="selection"
        width="45"
        :selectable="selecttable"
      ></el-table-column>
      <el-table-column
        prop="fsystem"
        label="系统"
        min-width="50"
      ></el-table-column>
      <el-table-column
        prop="fcomment"
        label="程序"
        min-width="80"
      ></el-table-column>
      <el-table-column
        prop="fslipno"
        label="联络票号"
        min-width="130"
      ></el-table-column>
      <el-table-column
        prop="fchkoutobj"
        label="文件名称"
        min-width="200"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        prop="fapplicant"
        label="申请者"
        min-width="60"
      ></el-table-column>
      <el-table-column
        prop="fregisterdte"
        label="申请日期"
        min-width="80"
      ></el-table-column>
      <el-table-column
        prop="fchkoutfile"
        label="迁出PBL"
        min-width="200"
        show-overflow-tooltip
      ></el-table-column>
      <el-table-column
        prop="fchkoutperson"
        label="迁出者"
        min-width="60"
      ></el-table-column>
      <el-table-column
        prop="fchkoutdte"
        label="迁出日期"
        min-width="80"
      ></el-table-column>
      <el-table-column
        prop="fchkinperson"
        label="迁入者"
        min-width="60"
      ></el-table-column>
      <el-table-column
        prop="fchkindte"
        label="迁入日期"
        min-width="80"
      ></el-table-column>
      <el-table-column prop="fchkstatus" label="状态" width="130">
        <template slot-scope="scope">
          <el-tag
            class="tag-style"
            :type="handleTag(scope.row)"
            v-if="!isCanModify(scope.row)"
            witch
            >{{ scope.row.fchkstatus }}</el-tag
          >
          <el-dropdown
            trigger="click"
            @command="updateStatus"
            v-if="isCanModify(scope.row)"
          >
            <el-tag class="tag-style" :type="handleTag(scope.row)">{{
              scope.row.fchkstatus
            }}</el-tag>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                disabled
                :command="beforeUpdateStatus('1-ASK', scope.row)"
                >1-ASK
              </el-dropdown-item>
              <el-dropdown-item
                disabled
                :command="beforeUpdateStatus('2-Check Out', scope.row)"
                >2-Check Out
              </el-dropdown-item>
              <el-dropdown-item
                :command="beforeUpdateStatus('3-Check In', scope.row)"
                >3-Check In
              </el-dropdown-item>
              <el-dropdown-item
                :command="beforeUpdateStatus('4-Un Check Out', scope.row)"
                >4-Un Check Out
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-link
            style="margin-left:10px"
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
            @click="openDialog('modify', scope.row.id)"
            v-show="isCanEdit(scope.row)"
          ></el-link>
          <el-link
            style="margin-left:20px"
            type="primary"
            :underline="false"
            icon="el-icon-delete"
            @click="singleDelete(scope.row.id)"
            v-show="isCanEdit(scope.row)"
          ></el-link>
        </template>
      </el-table-column>
    </el-table>
    <div>
      <el-pagination
        :hide-on-single-page="true"
        background
        layout="prev, pager, next"
        :total="checkoutTotal"
        :page-size="pageSize"
        :current-page="currentPage"
        :page-count="pageCount"
        @current-change="handlePage"
      >
      </el-pagination>
    </div>
    <CheckoutEdit
      ref="CheckoutEdit"
      @refreshCheckoutList="refreshCheckoutList"
    ></CheckoutEdit>
    <SendMailList ref="SendMailList"> </SendMailList>
  </div>
</template>

<script>
import {
  getCheckoutlistViaPagination,
  deleteCheckoutData,
  updateCheckoutData,
} from "../../../services/checkoutService";
import { getGroupUsers } from "../../../services/commonService";
import CheckoutEdit from "./CheckoutEdit";
import SendMailList from "./SendMailList";

export default {
  data() {
    return {
      checkoutTotal: 0,
      currentPage: 1,
      pageSize: 15,
      pageCount: 1,
      tableData: [],
      currentID: 0,
      systemList: [
        {
          value: "OMS",
          label: "OMS",
        },
        {
          value: "OMR",
          label: "OMR",
        },
        {
          value: "OMZ",
          label: "OMZ",
        },
        {
          value: "OMB",
          label: "OMB",
        },
        {
          value: "OMI",
          label: "OMI",
        },
        {
          value: "OMIIAB",
          label: "OMIIAB",
        },
        {
          value: "GCS",
          label: "GCS",
        },
      ],
      system: "",
      chkstatusList: [
        {
          value: "1-ASK",
          label: "1-ASK",
        },
        {
          value: "2-Check Out",
          label: "2-Check Out",
        },
        {
          value: "3-Check In",
          label: "3-Check In",
        },
        {
          value: "4-Un Check Out",
          label: "4-Un Check Out",
        },
      ],
      chkstatus: "",
      applicant: "",
      chkoutobj: "",
      slipno: "",
      userInfo: {},
      groupusers: {},
    };
  },
  components: {
    CheckoutEdit,
    SendMailList,
  },

  methods: {
    onQuery() {
      this.currentPage = 1;
      this.refreshCheckoutList();
    },

    onQueryAll() {
      this.currentPage = 1;
      this.system = "";
      this.chkstatus = "";
      this.applicant = "";
      this.chkoutobj = "";
      this.slipno = "";
      this.refreshCheckoutList();
    },

    onWorkSpace() {
      this.currentPage = 1;
      this.system = "";
      this.chkstatus = "";
      this.applicant = this.userInfo.name;
      this.chkoutobj = "";
      this.slipno = "";
      this.refreshCheckoutList();
    },

    handlePage(page) {
      this.currentPage = page;
      this.refreshCheckoutList();
    },

    calcPageTotal(listCount, pageSize) {
      listCount = this.checkoutTotal;
      pageSize = this.pageSize;
      var remainder = listCount % pageSize;
      if (remainder === 0) {
        this.pageCount = listCount / pageSize;
      } else {
        this.pageCount = parseInt(listCount / pageSize) + 1;
      }
    },

    async refreshCheckoutList() {
      this.tableData = [];
      var resp = await getCheckoutlistViaPagination(
        this.currentPage,
        this.pageSize,
        this.system,
        this.chkstatus,
        this.applicant,
        this.chkoutobj,
        this.slipno
      ).catch(() => {
        this.$message.error("Checkout数据获取异常");
        return;
      });

      var checkoutList = [];
      this.checkoutTotal = resp.data.count;
      this.calcPageTotal();
      checkoutList = resp.data.results;

      for (var i in checkoutList) {
        var id = checkoutList[i].id;
        var fregisterdte = checkoutList[i].fregisterdte;
        var fsystem = checkoutList[i].fsystem;
        var fcomment = checkoutList[i].fcomment;
        var fslipno = checkoutList[i].fslipno;
        var fchkoutobj = checkoutList[i].fchkoutobj;
        var fapplicant = checkoutList[i].fapplicant;
        var fchkstatus = checkoutList[i].fchkstatus;
        var fchkoutperson = checkoutList[i].fchkoutperson;
        var fchkoutdte = checkoutList[i].fchkoutdte;
        var fchkoutfile = checkoutList[i].fchkoutfile;
        var fchkinperson = checkoutList[i].fchkinperson;
        var fchkindte = checkoutList[i].fchkindte;

        var checkout = {
          id: id,
          fregisterdte: fregisterdte,
          fsystem: fsystem,
          fcomment: fcomment,
          fslipno: fslipno,
          fchkoutobj: fchkoutobj,
          fapplicant: fapplicant,
          fchkstatus: fchkstatus,
          fchkoutperson: fchkoutperson,
          fchkoutdte: fchkoutdte,
          fchkoutfile: fchkoutfile,
          fchkinperson: fchkinperson,
          fchkindte: fchkindte,
        };

        this.tableData.push(checkout);
      }
    },

    async batchDeleteCheckoutData() {
      var selectData = this.$refs.updateTable.selection;
      if (selectData.length > 0) {
        this.$confirm("此操作将永久删除选中的数据, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(async (action) => {
            if (action === "confirm") {
              for (var i in selectData) {
                var resp = await deleteCheckoutData(selectData[i].id).catch(
                  () => {
                    this.$message.error("CheckOut记录删除异常");
                  }
                );
                if (
                  Object.prototype.hasOwnProperty.call(resp.data, "message")
                ) {
                  this.$message.error(resp.data.message);
                }
              }
              this.refreshCheckoutList();
              this.$message({
                message: "批量删除成功！",
                type: "success",
              });
            }
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "取消删除",
            });
          });
      }
    },

    async singleDelete(id) {
      var resp = await deleteCheckoutData(id).catch(() => {
        this.$message.error("CheckOut记录删除异常");
      });
      if (resp.status === 204) {
        this.refreshCheckoutList();
        this.$message({
          message: "删除成功！",
          type: "success",
        });
      }
    },

    isCanEdit(row) {
      if (row.fchkstatus === "1-ASK") {
        return true;
      } else {
        return false;
      }
    },

    selecttable(row) {
      if (row.fchkstatus === "1-ASK") {
        return true;
      } else {
        return false;
      }
    },

    isCanModify(row) {
      if (row.fchkstatus === "2-Check Out") {
        return true;
      } else {
        return false;
      }
    },

    handleTag(row) {
      switch (row.fchkstatus) {
        case "1-ASK":
          return "";
        case "2-Check Out":
          return "warning";
        default:
          return "info";
      }
    },

    filterStatus(value, row) {
      return row.fchkstatus === value;
    },

    beforeUpdateStatus(item, row) {
      return {
        command: item,
        row: row,
      };
    },

    async updateStatus(command) {
      command.row.fchkstatus = command.command;
      var resp = await updateCheckoutData(command.row.id, command.row).catch(
        () => {
          this.$message.error("CheckOut记录状态更新异常");
        }
      );

      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("CheckOut记录状态更新成功");
      }

      this.refreshCheckoutList();
    },

    openDialog(model, id) {
      this.$refs.CheckoutEdit.init(model, id);
    },

    openSendMail() {
      this.$refs.SendMailList.init(this.userInfo.name);
    },
  },

  async mounted() {
    this.userInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.applicant = this.userInfo.name;
    this.refreshCheckoutList();

    var g_resp = await getGroupUsers().catch(() => {
      this.$message.error("分组用户主表数据获取异常");
      return;
    });
    this.groupusers = g_resp.data;
  },
};
</script>

<style>
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

.div-style {
  margin: 0px;
}

.tag-style {
  width: 100px;
}
</style>
