<template>
  <div>
    <el-table
      :data="testplan"
      border
      ref="testplan"
      style="width: 97%"
      size="medium"
      :cell-class-name="tableCellClassName"
      :highlight-current-row="true"
    >
      <el-table-column prop="target_tests" label="目标测试" min-width="80">
      </el-table-column>
      <el-table-column
        prop="target_regressions"
        label="目标回归测试"
        width="105"
      >
      </el-table-column>
      <el-table-column prop="target_total" label="目标总测试" min-width="90">
      </el-table-column>
      <el-table-column prop="target_ng" label="目标NG" min-width="70">
      </el-table-column>
      <el-table-column prop="actual_tests" label="实际测试" min-width="80">
      </el-table-column>
      <el-table-column
        prop="actual_regressions"
        label="实际回归测试"
        min-width="105"
      >
      </el-table-column>
      <el-table-column prop="actual_total" label="实际总测试" min-width="95">
      </el-table-column>
      <el-table-column prop="actual_ng" label="实际NG" min-width="75">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getQaHeadPlanActual } from "../../../services/qaService";
export default {
  data() {
    return {
      testplan: [],
    };
  },
  methods: {
    tableCellClassName({ row, columnIndex }) {
      var target_ng = row.target_ng;
      var target_regressions = row.target_regressions;
      var target_tests = row.target_tests;
      var target_total = row.target_total;
      var actual_ng = row.actual_ng;
      var actual_regressions = row.actual_regressions;
      var actual_tests = row.actual_tests;
      var actual_total = row.actual_total;
      if (columnIndex === 4) {
        if (actual_tests < target_tests) {
          return "warning-cell";
        }
        return "";
      } else if (columnIndex === 5) {
        if (actual_regressions < target_regressions) {
          return "warning-cell";
        }
        return "";
      } else if (columnIndex === 6) {
        if (actual_total < target_total) {
          return "warning-cell";
        }
        return "";
      } else if (columnIndex === 7) {
        if (actual_ng < target_ng) {
          return "warning-cell";
        } else if (actual_ng > target_ng * 1.2) {
          return "danger-cell";
        }
        return "";
      }
    },

    async refreshTargetActual() {
      var qahf_id = this.$route.query.qahf_id;
      this.testplan = []
      var plan_resp = await getQaHeadPlanActual(qahf_id).catch(() => {
        this.$message.error("生成测试计划实绩数据异常");
      });
      this.qahead_status = plan_resp.data.fstatus;
      this.testplan.push(plan_resp.data);
    },
  },
  mounted: async function() {
    await this.refreshTargetActual();
  },
};
</script>

<style>
.warning-cell{
  background-color: #ffd3b4;
}
.danger-cell{
  background-color: #ffaaa7;
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
