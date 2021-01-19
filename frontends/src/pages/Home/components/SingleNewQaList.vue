<template>
  <el-dialog title="逐条添加测试用例" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item prop="fcontent" required>
        <el-input
          v-model="form.fcontent"
          type="textarea"
          :rows="3"
          placeholder="测试用例"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-col :span="12">
          <el-form-item prop="fclass1">
            <el-input
              v-model="form.fclass1"
              class="width-sytle"
              placeholder="分类(非必输)"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="fsortrule">
            <el-input
              v-model="form.fsortrule"
              class="width-sytle"
              placeholder="排序规则(非必输)"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item prop="fregression">
            <el-checkbox
              v-model="form.fregression"
              border
              true-label="Y"
              false-label="N"
              >回归测试</el-checkbox
            >
          </el-form-item>
        </el-col>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="onSubmit('form')">确 定</el-button>
      <el-button @click="resetForm('form')">重 置</el-button>
      <el-button @click="dialogFormVisible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { newQaDetail } from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      form: {
        fclass1: "",
        fregression: "N",
        fcontent: "",
        fsortrule: "",
        qahf: "",
      },
      rules: {
        fcontent: [
          { required: true, message: "请输入测试用例", trigger: "change" },
        ],
        fregression: [{ required: false }],
        fclass1: [{ required: false }],
        fsortrule: [{ required: false }],
      },
    };
  },
  methods: {
    handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      this.form.qahf = id;
    },
    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await newQaDetail(this.form).catch(() => {
            this.$message.error("逐条添加测试项异常");
          });

          if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.$message.error(resp.data.message);
          } else {
            this.$emit("refreshQaList");
            this.dialogFormVisible = false;
            this.resetForm("form");
            this.$message({
              message: this.form.fcontent + "创建成功！",
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

<style scoped>
.width-sytle {
  width: 90%;
}
</style>
