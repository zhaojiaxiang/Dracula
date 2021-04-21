<template>
  <div>
    <el-table
      :data="testplan"
      border
      ref="testplan"
      style="width: 95%"
      size="medium"
      :cell-class-name="tableCellClassName"
      :highlight-current-row="true"
    >
      <el-table-column prop="actual_tests" label="实际测试数" min-width="110">
      </el-table-column>
      <el-table-column prop="actual_ng" label="实际NG数" min-width="100">
      </el-table-column>
      <el-table-column prop="actual_ngok" label="实际NGOK数" min-width="110">
      </el-table-column>
      <el-table-column prop="actual_ng_rate" label="测试检出率" min-width="110">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getQaHeadPlanActual } from "./../../../services/qaService";
export default {
  data() {
    return {
      testplan: [],
    };
  },

  methods: {
    tableCellClassName({ row, columnIndex }) {
      if (columnIndex === 3) {
        var actual_ng_rate = row.actual_ng_rate;
        actual_ng_rate = actual_ng_rate.replace("%", "");
        actual_ng_rate = parseFloat(actual_ng_rate);
        if ((actual_ng_rate > 10) | (actual_ng_rate < 5)) {
          return "danger-cell";
        }
        return "";
      }
    },

    async refreshTargetActual() {
      var qahf_id = this.$route.query.qahf_id;
      this.testplan = [];
      var plan_resp = await getQaHeadPlanActual(qahf_id).catch(() => {
        this.$message.error("生成测试计划实绩数据异常");
      });
      this.qahead_status = plan_resp.data.fstatus;
      this.testplan.push(plan_resp.data);
    },
  },

  mounted: function() {
    this.refreshTargetActual();
  },
};
</script>

<style>
.warning-cell {
  background-color: #ffd3b4;
}
.danger-cell {
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
