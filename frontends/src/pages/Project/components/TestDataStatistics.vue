<template>
  <el-dialog :visible.sync="dialogFormVisible" width="95%">
    <el-table
      :data="testplan"
      border
      ref="testplan"
      style="width: 100%"
      max-height="500"
      size="medium"
      :summary-method="getNGSummaries"
      show-summary
      :cell-class-name="tableCellClassName"
      :highlight-current-row="true"
    >
      <el-table-column
        prop="slip_no"
        label="联络票号"
        min-width="150"
        :filters="slip_filters"
        :filter-method="filterSlipNo"
        filter-placement="bottom-end"
      >
      </el-table-column>
      <el-table-column
        prop="assigned_to"
        label="对应者"
        min-width="70"
        :filters="assigned_filters"
        :filter-method="filterSlipAssignedto"
        filter-placement="bottom-end"
      >
      </el-table-column>
      <el-table-column prop="total_lines" label="影响总行数" min-width="95">
      </el-table-column>
      <el-table-column prop="modify_lines" label="修改总行数" min-width="95">
      </el-table-column>
      <el-table-column prop="target_tests" label="目标测试" min-width="80">
      </el-table-column>
      <el-table-column
        prop="target_regressions"
        label="目标回归测试"
        width="105"
      >
      </el-table-column>
      <el-table-column prop="target_total" label="目标总测试" min-width="95">
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
      <el-table-column prop="actual_ng_rate" label="NG率" min-width="75">
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { getTestStatistics } from "../../../services/liaisonService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      testplan: [],
      slip_filters: [],
      assigned_filters: [],
    };
  },
  methods: {
    filterSlipNo(value, row) {
      return row.slip_no === value;
    },

    filterSlipAssignedto(value, row) {
      return row.assigned_to === value;
    },

    getNGSummaries(param) {
      const { columns, data } = param;
      const sums = [];
      columns.forEach((column, index) => {
        const values = data.map((item) => Number(item[column.property]));
        if (!values.every((value) => isNaN(value))) {
          sums[index] = values.reduce((prev, curr) => {
            const value = Number(curr);
            if (!isNaN(value)) {
              return prev + curr;
            } else {
              return prev;
            }
          }, 0);
          sums[index];
        } else {
          sums[index] = "";
        }

        if (index === 0) {
          sums[index] = "统计和";
          return;
        }

        if (index === 12) {
          sums[index] = (sums[11] / sums[10]).toFixed(4) * 100 + "%";
          return;
        }
      });

      return sums;
    },

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
          return "table-cell-warning";
        }
        return "";
      } else if (columnIndex === 5) {
        if (actual_regressions < target_regressions) {
          return "table-cell-warning";
        }
        return "";
      } else if (columnIndex === 6) {
        if (actual_total < target_total) {
          return "table-cell-warning";
        }
        return "";
      } else if (columnIndex === 7) {
        if (actual_ng < target_ng) {
          return "table-cell-warning";
        } else if (actual_ng > target_ng * 1.2) {
          return "table-cell-danger";
        }
        return "";
      }
    },

    async handleDialog(order_no) {
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getTestStatistics(order_no).catch(() => {
        this.$message.error("测试统计数据获取异常");
      });
      this.testplan = resp.data;

      this.testplan.forEach((element) => {
        var isExisted = false;
        var slip_json = {};
        var assigned_json = {};
        slip_json.text = element.slip_no;
        slip_json.value = element.slip_no;

        this.slip_filters.push(slip_json);

        assigned_json.text = element.assigned_to;
        assigned_json.value = element.assigned_to;

        for (var i in this.assigned_filters) {
          if (this.assigned_filters[i].text === element.assigned_to) {
            isExisted = true;
            continue;
          }
        }

        if (!isExisted) {
          this.assigned_filters.push(assigned_json);
        }
      });
    },
  },
};
</script>

<style></style>
