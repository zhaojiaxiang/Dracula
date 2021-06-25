<template>
  <div class="div-style-2">
    <el-row style="margin-bottom: 5px">
      <el-col :span="12">
        <Guide>
          <template>
            <div>
              <h5><strong>联络票&单体测试</strong></h5>
            </div>
          </template>
        </Guide>
      </el-col>

      <el-col :span="12">
        <div style="text-align: right">
          <el-button @click="openTestStatistics">测试数据统计</el-button>
        </div>
      </el-col>
    </el-row>
    <el-table
      border
      :data="tableData"
      style="width: 100%"
      :height="tableHeight"
      :span-method="arraySpanMethod"
      size="medium"
      class="card-shadow"
    >
      <el-table-column
        prop="slip_status"
        label="状态"
        fixed
        width="80"
        :filters="slip_status_filters"
        :filter-method="filterSlipStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag
            :class="statusTagClass(scope.row.slip_status)"
            disable-transitions
            >{{ scope.row.slip_status }}</el-tag
          >
        </template>
      </el-table-column>
      <el-table-column
        fixed
        prop="slip_slip"
        label="联络票号"
        min-width="150"
        :filters="slip_slip_filters"
        :filter-method="filterSlipNo"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>开发概要: {{ scope.row.slip_brief }}</p>
            <p>问题描述: {{ scope.row.slip_content }}</p>
            <p>问题分析: {{ scope.row.slip_analyse }}</p>
            <p>解决方案: {{ scope.row.slip_solution }}</p>
            <p>计划工时: {{ scope.row.slip_plnmanpower }}</p>
            <p>实际工时: {{ scope.row.slip_actmanpower }}</p>
            <div slot="reference" class="name-wrapper">
              {{ scope.row.slip_slip }}
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        prop="slip_assignedto"
        label="对应者"
        min-width="80"
        :filters="slip_assignedto_filters"
        :filter-method="filterSlipAssignedto"
        filter-placement="bottom-end"
      >
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
            :type="linkStyle(scope.row.design_id)"
            :underline="false"
            v-show="designShow(scope.row.slip_type, scope.row.design_id)"
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
        min-width="180"
        fixed="right"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <el-link
            @click="openQaList(scope.row.qa_id)"
            type="primary"
            :underline="false"
            >{{ scope.row.qa_object }}</el-link
          >
        </template>
      </el-table-column>
      <el-table-column
        prop="qa_status"
        label="状态"
        width="80"
        fixed="right"
        :filters="qa_status_filters"
        :filter-method="filterQAStatus"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag :type="scope.row.qa_tagtype" disable-transitions>{{
            scope.row.qa_status
          }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column
        fixed="right"
        prop="qa_modification"
        label="概要"
        min-width="60"
      >
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
      <el-table-column
        fixed="right"
        prop="code_id"
        label="代码Review"
        min-width="100"
      >
        <template slot-scope="scope">
          <el-link
            :underline="false"
            :type="linkStyle(scope.row.code_id)"
            @click="openCodeReview(scope.row.slip_slip, scope.row.qa_object)"
            >代码Review</el-link
          >
        </template>
      </el-table-column>
      <!-- <el-table-column fixed="right" label="操作" width="80">
        <template slot-scope="scope">
          <el-link
            @click="openQaList(scope.row.qa_id)"
            type="primary"
            :underline="false"
            icon="el-icon-edit-outline"
          ></el-link>
        </template>
      </el-table-column> -->
    </el-table>
    <QaObjectSummary
      ref="QaObjectSummary"
      :isdisable="isdisable"
    ></QaObjectSummary>

    <QaDesignReview
      ref="QaDesignReview"
      :isdisable="isdisable"
    ></QaDesignReview>
    <QaCodeReview ref="QaCodeReview" :isdisable="isdisable"></QaCodeReview>
    <TestDataStatistics ref="TestDataStatistics"></TestDataStatistics>
  </div>
</template>

<script>
import QaObjectSummary from "./../../Home/components/QaObjectSummary";
import QaDesignReview from "./../../Home/components/QaDesignReview";
import QaCodeReview from "./../../Home/components/QaCodeReview";
import TestDataStatistics from "../components/TestDataStatistics";
import Guide from "./../../Home/components/Guide";
import { getProjectDetailView } from "../../../services/projectService";
export default {
  components: {
    QaObjectSummary,
    QaDesignReview,
    QaCodeReview,
    Guide,
    TestDataStatistics,
  },
  data() {
    return {
      order_no: "",
      isdisable: false,
      tableHeight: 100,
      spanArr: [],
      pos: 0,
      tableData: [],
      slip_status_filters: [],
      qa_status_filters: [],
      slip_slip_filters: [],
      slip_assignedto_filters: [],
    };
  },
  methods: {
    openTestStatistics() {
      this.$refs.TestDataStatistics.handleDialog(this.order_no);
    },

    linkStyle(id) {
      if (id) {
        return "success";
      } else {
        return "danger";
      }
    },

    designShow(type, id){
      if(type==='追加开发'){
        return true
      }else{
        if(id){
          return true
        }
      }
      return false
    },

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

    filterSlipNo(value, row) {
      return row.slip_slip === value;
    },

    filterSlipAssignedto(value, row) {
      return row.slip_assignedto === value;
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

    async refreshProjectDetailView() {
      this.tableData = [];
      var resp = await getProjectDetailView(this.order_no).catch(() => {
        this.$message.error("联络票数据获取异常");
        return;
      });

      var projectView = [];
      projectView = resp.data;

      for (var i in projectView) {
        var slip_json = {};
        var assignedto_json = {};
        var slip_status_json = {};
        var qa_status_json = {};

        var isSlipExisted = false;
        var isAssignedtoExisted = false;
        var isSlipStatusExisted = false;
        var isQAStatusExisted = false;

        var slip_id = projectView[i].slip_id;
        var slip_slip = projectView[i].slip_slip;
        var slip_type = projectView[i].slip_type;
        var slip_status = projectView[i].slip_status;
        var slip_brief = projectView[i].slip_brief;
        var slip_content = projectView[i].slip_content;
        var slip_analyse = projectView[i].slip_analyse;
        var slip_solution = projectView[i].slip_solution;
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
          slip_type: slip_type,
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
          slip_content,
          slip_analyse,
          slip_solution,
        };

        slip_json.text = slip_slip;
        slip_json.value = slip_slip;

        assignedto_json.text = slip_assignedto;
        assignedto_json.value = slip_assignedto;

        slip_status_json.text = slip_status;
        slip_status_json.value = slip_status;

        qa_status_json.text = qa_status;
        qa_status_json.value = qa_status;

        for (var j in this.slip_slip_filters) {
          if (this.slip_slip_filters[j].text === slip_slip) {
            isSlipExisted = true;
            continue;
          }
        }

        if (!isSlipExisted) {
          this.slip_slip_filters.push(slip_json);
        }

        for (var k in this.slip_assignedto_filters) {
          if (this.slip_assignedto_filters[k].text === slip_assignedto) {
            isAssignedtoExisted = true;
            continue;
          }
        }

        if (!isAssignedtoExisted) {
          this.slip_assignedto_filters.push(assignedto_json);
        }

        for (var l in this.slip_status_filters) {
          if (this.slip_status_filters[l].text === slip_status) {
            isSlipStatusExisted = true;
            continue;
          }
        }

        if (!isSlipStatusExisted) {
          this.slip_status_filters.push(slip_status_json);
        }

        for (var m in this.qa_status_filters) {
          if (this.qa_status_filters[m].text === qa_status) {
            isQAStatusExisted = true;
            continue;
          }
        }

        if (!isQAStatusExisted) {
          this.qa_status_filters.push(qa_status_json);
        }

        this.tableData.push(project);

        this.getSpanArr(this.tableData);
      }

      var clientHeight = document.documentElement.clientHeight;
      var maxHeight = 600;

      this.tableHeight = this.tableData.length * 43 + 100;
      if (clientHeight > 900) {
        maxHeight = 600;
      } else {
        maxHeight = 350;
      }

      if (this.tableHeight > maxHeight) {
        this.tableHeight = maxHeight;
      }
    },
  },
  mounted: function () {
    this.order_no = this.$route.query.order_no;
    this.refreshProjectDetailView();
  },
};
</script>

<style>
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
.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
.div-style-2 {
  margin: 0px;
  background-color: #f0f2f5;
}
</style>
