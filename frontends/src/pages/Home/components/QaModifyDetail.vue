<template>
  <el-dialog
    title="测试对象修改明细"
    lock-scroll
    :visible.sync="dialogFormVisible"
  >
    <el-form ref="form" label-width="20%" :rules="rules" :model="form">
      <el-form-item prop="fttlcodelines" label="影响总行数:" required>
        <el-input
          v-model="form.fttlcodelines"
          placeholder="影响总行数"
          type="number"
        ></el-input>
      </el-form-item>
      <el-form-item prop="fmodifiedlines" label="修改行数:" required>
        <el-input
          v-model="form.fmodifiedlines"
          placeholder="修改行数"
          type="number"
        ></el-input>
      </el-form-item>
      <el-form-item prop="fcomplexity" label="复杂度:" required>
        <el-radio-group v-model="form.fcomplexity">
          <el-radio-button label="0.8"></el-radio-button>
          <el-radio-button label="1.0"></el-radio-button>
          <el-radio-button label="1.2"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item prop="fselflevel" label="自我评价难易等级:">
        <el-select v-model="form.fselflevel" placeholder="请选择难易等级">
          <el-option label="01" value="01"></el-option>
          <el-option label="02" value="02"></el-option>
          <el-option label="03" value="03"></el-option>
          <el-option label="04" value="04"></el-option>
          <el-option label="05" value="05"></el-option>
          <el-option label="06" value="06"></el-option>
          <el-option label="07" value="07"></el-option>
          <el-option label="08" value="08"></el-option>
          <el-option label="09" value="09"></el-option>
          <el-option label="10" value="10"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button
        type="primary"
        v-show="qahead_status === '1' || qahead_status === '2'"
        @click="onSubmit('form')"
        >确 定</el-button
      >
      <el-button @click="resetForm('form')">重 置</el-button>
      <el-button @click="dialogFormVisible = false">取 消</el-button>
    </div>
    <el-table
      :data="testplan"
      border
      ref="testplan"
      :cell-class-name="tableCellClassName"
      style="width: 100%"
      :highlight-current-row="true"
    >
      <el-table-column prop="target_tests" label="目标测试数" width="95">
      </el-table-column>
      <el-table-column
        prop="target_regressions"
        label="目标回归测试数"
        width="120"
      >
      </el-table-column>
      <el-table-column prop="target_total" label="目标总测试数" width="120">
      </el-table-column>
      <el-table-column prop="target_ng" label="目标NG数" width="95">
      </el-table-column>
      <el-table-column prop="actual_tests" label="实际测试数" width="100">
      </el-table-column>
      <el-table-column
        prop="actual_regressions"
        label="实际回归测试数"
        width="120"
      >
      </el-table-column>
      <el-table-column prop="actual_total" label="实际总测试数" width="120">
      </el-table-column>
      <el-table-column
        prop="actual_ng"
        label="实际NG数"
        width="100"
      >
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import {
  updateQaHeadModifyDetail,
  getQaHeadModifyDetail,
  getQaHeadPlanActual,
} from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      testplan: [],
      qahead_status: "",
      form: {
        id: "",
        fttlcodelines: "",
        fmodifiedlines: "",
        fcomplexity: "",
        fselflevel:"",
      },
      rules: {
        fttlcodelines: [
          { required: true, message: "请输入影响总行数", trigger: "change" },
        ],
        fmodifiedlines: [
          { required: true, message: "请输入修改行数", trigger: "change" },
        ],
        fcomplexity: [
          { required: true, message: "请选择复杂度", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    tableCellClassName({row, columnIndex}) {
      var target_ng = row.target_ng
      var target_regressions = row.target_regressions
      var target_tests = row.target_tests
      var target_total = row.target_total
      var actual_ng = row.actual_ng
      var actual_regressions = row.actual_regressions
      var actual_tests = row.actual_tests
      var actual_total = row.actual_total
      if (columnIndex === 4) {
        if(actual_tests < target_tests ){
          return "table-cell-warning";
        }
        return ''
      } else if(columnIndex === 5){
        if(actual_regressions < target_regressions ){
          return "table-cell-warning";
        }
        return ''
      }else if(columnIndex === 6){
        if(actual_total < target_total ){
          return "table-cell-warning";
        }
        return ''
      }else if(columnIndex === 7){
        if(actual_ng < target_ng ){
          return "table-cell-warning";
        }else if( actual_ng  > target_ng * 1.2 ){
          return "table-cell-danger";
        }
        return ''
      }
    },

    async handleDialog(id) {
      this.testplan = [];
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getQaHeadModifyDetail(id).catch(() => {
        this.$message.error("测试对象修改明细获取异常");
      });

      this.form = resp.data;

      var plan_resp = await getQaHeadPlanActual(id).catch(() => {
        this.$message.error("生成测试计划实绩数据异常");
      });
      this.qahead_status = plan_resp.data.fstatus;
      this.testplan.push(plan_resp.data);
    },
    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await updateQaHeadModifyDetail(
            this.form.id,
            this.form
          ).catch(() => {
            this.$message.error("测试对象修改明细更新异常");
          });
          if (resp.status === 200) {
            this.$emit("refreshQaList");
            this.dialogFormVisible = false;
            this.resetForm("form");
            this.$message({
              message: "修改成功！",
              type: "success",
            });
          }
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style>
.width-sytle {
  width: 90%;
}
.el-dialog__body {
  padding-top: 0;
  padding-bottom: 0;
}

.table-cell-danger {
  background: #f5c6cb;
}
.table-cell-warning {
  background: #ffeeba;
}
</style>
