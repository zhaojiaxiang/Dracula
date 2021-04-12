<template>
  <div class="div-style">
    <el-table
      border
      :data="tableData"
      style="width: 100%"
      :height="tableHeight"
      :span-method="arraySpanMethod"
      size="medium"
    >
      <el-table-column
        prop="slip_status"
        label="状态"
        fixed
        width="80"
        :filters="[
          { text: '待办', value: '待办' },
          { text: '进行中', value: '进行中' },
          { text: '已完成', value: '已完成' },
          { text: '已发布', value: '已发布' },
        ]"
        :filter-method="filterSlipStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag type="primary" disable-transitions>{{
            scope.row.slip_status
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed prop="slip_slip" label="联络票号" min-width="150">
      </el-table-column>
      <el-table-column prop="slip_assignedto" label="对应者" min-width="70">
      </el-table-column>
      <el-table-column
        prop="slip_brief"
        label="详情"
        min-width="250"
        show-overflow-tooltip
      >
      </el-table-column>
      <el-table-column prop="design_id" label="设计Review" min-width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            v-show="scope.row.design_id"
            @click="openDesignReview(scope.row.slip_slip)"
            >设计Review</el-link
          >
        </template>
      </el-table-column>
      <el-table-column prop="slip_plan" label="计划" width="210">
      </el-table-column>
      <el-table-column prop="slip_actual" label="实际" width="210">
      </el-table-column>
      <el-table-column prop="slip_release" label="发布" width="100">
      </el-table-column>
      <el-table-column
        prop="qa_object"
        label="测试对象"
        min-width="150"
        show-overflow-tooltip
      >
      </el-table-column>
      <el-table-column
        prop="qa_status"
        label="状态"
        width="80"
        :filters="[
          { text: '初始', value: '初始' },
          { text: '已审核', value: '已审核' },
          { text: '已提交', value: '已提交' },
          { text: '已确认', value: '已确认' },
        ]"
        :filter-method="filterQAStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.qa_tagtype" disable-transitions>{{
            scope.row.qa_status
          }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="qa_modification" label="概要" min-width="60">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            v-show="scope.row.qa_modification"
            @click="openObjectSummary(scope.row.qa_id)"
            >概要</el-link
          >
        </template>
      </el-table-column>
      <el-table-column prop="code_id" label="代码Review" min-width="100">
        <template slot-scope="scope">
          <el-link
            type="primary"
            :underline="false"
            v-show="scope.row.code_id"
            @click="openCodeReview(scope.row.slip_slip, scope.row.qa_object)"
            >代码Review</el-link
          >
        </template>
      </el-table-column>

      <el-table-column fixed="right" label="操作" width="60">
        <template slot-scope="scope">
          <el-link
            @click="openQaList(scope.row.qa_id)"
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
          ></el-link>
        </template>
      </el-table-column>
    </el-table>
    <QaObjectSummary ref="QaObjectSummary"></QaObjectSummary>

    <QaDesignReview
      ref="QaDesignReview"
      :isdisable="isdisable"
    ></QaDesignReview>
    <QaCodeReview ref="QaCodeReview" :isdisable="isdisable"></QaCodeReview>
  </div>
</template>

<script>
import QaObjectSummary from "./../../Home/components/QaObjectSummary";
import QaDesignReview from "./../../Home/components/QaDesignReview";
import QaCodeReview from "./../../Home/components/QaCodeReview";
import { getProjectDetailView } from "../../../services/projectService";
export default {
  components: {
    QaObjectSummary,
    QaDesignReview,
    QaCodeReview,
  },
  data() {
    return {
      order_no: "",
      isdisable: true,
      tableHeight: 100,
      spanArr: [],
      pos: 0,
      tableData: [],
    };
  },
  methods: {
    getSpanArr(data) {
      this.spanArr = [];
      if (data === null) {
        return;
      }
      for (var i = 0; i < data.length; i++) {
        if (i === 0) {
          this.spanArr.push(1);
          this.pos = 0;
        } else {
          if (data[i].slip_id === data[i - 1].slip_id) {
            // 如果ID一样则需要进行合并
            this.spanArr[this.pos] += 1;
            this.spanArr.push(0);
          } else {
            this.spanArr.push(1);
            this.pos = i;
          }
        }
      }
    },

    arraySpanMethod({ rowIndex, columnIndex }) {
      // 合并的列数
      if (
        columnIndex === 0 ||
        columnIndex === 1 ||
        columnIndex === 2 ||
        columnIndex === 3 ||
        columnIndex === 4 ||
        columnIndex === 5 ||
        columnIndex === 6 ||
        columnIndex === 7
      ) {
        const _row = this.spanArr[rowIndex]; // 从处理完的数组里获取
        const _col = _row > 0 ? 1 : 0;
        return {
          rowspan: _row,
          colspan: _col, // 相当于给给表格加上rowspan,colspan属性
        };
      }
    },

    filterSlipStatus(value, row) {
      return row.slip_status === value;
    },

    filterQAStatus(value, row) {
      return row.qa_status === value;
    },

    openObjectSummary(id) {
      this.$refs.QaObjectSummary.handleDialog(id);
    },

    openDesignReview(slipno) {
      this.$refs.QaDesignReview.handleDialog(slipno);
    },

    openCodeReview(slipno, objectid) {
      this.$refs.QaCodeReview.handleDialog(slipno, objectid);
    },

    openQaList(qahf_id) {
      this.$router.push({
        name: "ProjectOverviewQA",
        query: { qahf_id: qahf_id },
      });
    },

    async refreshProjectDetailView() {
      this.tableData = [];
      var resp = await getProjectDetailView(this.order_no).catch(() => {
        this.$message.error("联络票数据获取异常");
        return;
      });

      var projectView = [];
      projectView = resp.data;

      for (var i in projectView) {
        var slip_id = projectView[i].slip_id;
        var slip_slip = projectView[i].slip_slip;
        var slip_status = projectView[i].slip_status;
        var slip_brief = projectView[i].slip_brief;
        var slip_assignedto = projectView[i].slip_assignedto;
        var slip_plnstart = projectView[i].slip_plnstart;
        var slip_plnend = projectView[i].slip_plnend;
        var slip_actstart = projectView[i].slip_actstart;
        var slip_actend = projectView[i].slip_actend;
        var slip_release = projectView[i].slip_release;
        var slip_plnmanpower = projectView[i].slip_plnmanpower;
        var slip_actmanpower = projectView[i].slip_actmanpower;
        var design_id = projectView[i].design_id;
        var qa_id = projectView[i].qa_id;
        var qa_object = projectView[i].qa_object;
        var qa_status = projectView[i].qa_status;
        var qa_modification = projectView[i].qa_modification;
        var code_id = projectView[i].code_id;

        var slip_plan = slip_plnstart + " ~ " + slip_plnend;
        var slip_actual = "";

        if (slip_status === "1") {
          slip_status = "待办";
        } else if (slip_status === "2") {
          slip_status = "进行中";
          slip_actual = slip_actstart;
        } else if (slip_status === "3") {
          slip_status = "已完成";
          slip_actual = slip_actstart + " ~ " + slip_actend;
        } else if (slip_status === "4") {
          slip_status = "已发布";
          slip_actual = slip_actstart + " ~ " + slip_actend;
        }

        var qa_tagtype = "";

        if (qa_status === "1") {
          qa_status = "初始";
          qa_tagtype = "info";
        } else if (qa_status === "2") {
          qa_status = "已审核";
          qa_tagtype = "";
        } else if (qa_status === "3") {
          qa_status = "已提交";
          qa_tagtype = "warning";
        } else if (qa_status === "4") {
          qa_status = "已确认";
          qa_tagtype = "success";
        }

        var project = {
          slip_id: slip_id,
          slip_slip: slip_slip,
          slip_status: slip_status,
          slip_brief: slip_brief,
          slip_assignedto: slip_assignedto,
          slip_plan: slip_plan,
          slip_actual: slip_actual,
          slip_release: slip_release,
          slip_plnmanpower: slip_plnmanpower,
          slip_actmanpower: slip_actmanpower,
          design_id: design_id,
          qa_id: qa_id,
          qa_object: qa_object,
          qa_status: qa_status,
          qa_tagtype: qa_tagtype,
          qa_modification: qa_modification,
          code_id: code_id,
        };
        this.tableData.push(project);

        this.getSpanArr(this.tableData);

        this.tableHeight = this.tableData.length * 43 + 47;
        if (this.tableHeight > 600) {
          this.tableHeight = 600;
        }
      }
    },
  },
  mounted: function() {
    this.order_no = this.$route.query.order_no;
    this.refreshProjectDetailView();
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
</style>
