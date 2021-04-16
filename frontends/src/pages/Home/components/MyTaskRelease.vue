<template>
  <div class="div-style">
    <div style="margin:10px">
      <el-page-header @back="goBack"> </el-page-header>
    </div>
    <el-table
      :data="tableData"
      class="card-shadow"
      style="width: 100%"
      size="medium"
    >
      <el-table-column
        prop="fstatus"
        label="状态"
        fixed
        width="80"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-dropdown trigger="click" @command="handleStatus">
            <el-tag
              :class="statusTagClass(scope.row.fstatus)"
              disable-transitions
              >{{ scope.row.fstatus }}</el-tag
            >
            <el-dropdown-menu slot="dropdown">
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
      <el-table-column
        fixed
        prop="fassignedto"
        label="对应者"
        min-width="90"
        :filters="user_filters"
        :filter-method="filterUser"
        filter-placement="bottom-end"
      >
      </el-table-column>
      <el-table-column
        fixed
        prop="fodrno"
        label="订单号"
        min-width="160"
        :filters="order_filters"
        :filter-method="filterOrder"
        filter-placement="bottom-end"
      >
      </el-table-column>
      <el-table-column fixed prop="fslipno" label="联络票号" min-width="160">
      </el-table-column>
      <el-table-column
        prop="fbrief"
        label="详情"
        min-width="370"
        show-overflow-tooltip
      >
      </el-table-column>
      <el-table-column prop="actual" label="实际" width="220">
      </el-table-column>
      <el-table-column prop="factmanpower" label="实际工时" width="100">
      </el-table-column>

      <el-table-column prop="factmanpower" label="变更报表" width="100">
        <template slot-scope="scope">
          <el-link :underline="false" :icon="scope.row.icon"></el-link>
        </template>
      </el-table-column>

      <el-table-column fixed="right" label="操作" width="120">
        <template slot-scope="scope">
          <el-upload
            class="upload-demo"
            action="/api/file_upload/"
            :before-upload="beforeFileUpload"
            :limit="1"
          >
            <el-link
              :underline="false"
              icon="el-icon-upload2"
              @click="cellclick(scope.row.id)"
              >上传</el-link
            >
          </el-upload>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {
  getMyRelease,
  updateLiaisonStatus,
  getSingleLiaison,
} from "../../../services/liaisonService";
import { liaisonfileUpdate } from "../../../services/liaisonService";
export default {
  data() {
    return {
      currentID: 0,
      tableData: [],
      user_filters: [],
      order_filters: [],
    };
  },
  methods: {
    typeTagClass(type) {
      if (type === "追加开发") {
        return "success";
      } else if (type === "改善需求") {
        return "warning";
      } else {
        return "danger";
      }
    },

    statusTagClass(status) {
      if (status === "待办") {
        return "status-1";
      } else if (status === "进行中") {
        return "status-2";
      } else if (status === "已完成") {
        return "status-3";
      } else {
        return "status-4";
      }
    },

    filterUser(value, row) {
      return row.fassignedto === value;
    },

    filterSlip(value, row) {
      return row.fslipno === value;
    },

    filterOrder(value, row) {
      return row.fodrno === value;
    },

    filterType(value, row) {
      return row.ftype === value;
    },
    goBack() {
      window.history.go(-1);
    },
    cellclick(id) {
      this.currentID = id;
    },
    async refreshLiaisons() {
      this.tableData = [];
      // var resp = await getLiaisons();
      var resp = await getMyRelease().catch(() => {
        this.$message.error("待发布联络票数据获取异常");
        return;
      });

      var liaisons = [];

      this.liaisonTotal = resp.data.count;
      liaisons = resp.data;

      for (var i in liaisons) {
        var isUserExisted = false;
        var isOrderExisted = false;
        var user_json = {};
        var order_json = {};

        var id = liaisons[i].id;
        var ftype = liaisons[i].ftype;
        var fstatus = liaisons[i].fstatus;
        var fslipno = liaisons[i].fslipno;
        var fodrno = liaisons[i].fodrno;
        var fassignedto = liaisons[i].fassignedto;
        var fbrief = liaisons[i].fbrief;
        var factstart = liaisons[i].factstart;
        var factend = liaisons[i].factend;
        var freleasedt = liaisons[i].freleasedt;
        var factmanpower = liaisons[i].factmanpower;
        var freleaserpt = liaisons[i].freleaserpt;
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
        var icon;
        if (freleaserpt) {
          icon = "el-icon-document-checked";
        } else {
          icon = "";
        }

        user_json.text = fassignedto;
        user_json.value = fassignedto;

        order_json.text = fodrno;
        order_json.value = fodrno;

        for (var k in this.user_filters) {
          if (this.user_filters[k].text === fassignedto) {
            isUserExisted = true;
            continue;
          }
        }

        if (!isUserExisted) {
          this.user_filters.push(user_json);
        }

        for (var l in this.order_filters) {
          if (this.order_filters[l].text === fodrno) {
            isOrderExisted = true;
            continue;
          }
        }

        if (!isOrderExisted) {
          this.order_filters.push(order_json);
        }

        var liaison = {
          id: id,
          ftype: ftype,
          fstatus: fstatus,
          fslipno: fslipno,
          fodrno: fodrno,
          fassignedto: fassignedto,
          fbrief: fbrief,
          actual: actual,
          freleasedt: "media/upload/file/" + freleasedt,
          factmanpower: factmanpower,
          icon: icon,
        };
        this.tableData.push(liaison);
      }
    },

    async beforeFileUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;

      let fileForm = new FormData();

      if (!isLt2M) {
        this.$message.error("上传文件大小不能超过 2MB!");
      }

      fileForm.append("file", file);
      fileForm.append("liaison", this.currentID);

      var resp = await liaisonfileUpdate(fileForm).catch(() => {
        this.$message.error("文件上传到服务器异常");
      });

      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("文件上传成功");
        this.refreshLiaisons();
      }
    },

    async handleStatus(command) {
      var get_resp = await getSingleLiaison(command.row.id).catch(() => {
        this.$message.error("联络票数据获取异常");
        return;
      });
      if (get_resp.status === 200) {
        var liaison = get_resp.data;
        var status = command.command;
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

        if (Object.prototype.hasOwnProperty.call(put_resp.data, "message")) {
          this.$message.error(put_resp.data.message);
          return;
        } else {
          this.$emit("refreshHome");
          this.$message({
            message: command.row.fslipno + "发布成功",
            type: "success",
          });
          this.refreshLiaisons();
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
  },
  mounted: function() {
    this.refreshLiaisons();
  },
};
</script>

<style>
.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
.status-1 {
  background-color: #fbe6d4;
  border-color: #fbe6d4;
  color: #ffa931;
}
.status-2 {
  background-color: #fecb89;
  border-color: #fecb89;
  color: #fff;
}
.status-3 {
  background-color: #ffa931;
  color: #fff;
  border-color: #ffa931;
}
.status-4 {
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
.div-style {
  margin: 0px;
}
</style>
