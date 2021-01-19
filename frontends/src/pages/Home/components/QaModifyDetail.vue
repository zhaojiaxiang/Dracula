<template>
  <el-dialog title="测试对象修改明细" :visible.sync="dialogFormVisible">
    <el-form ref="form" label-width="20%" :rules="rules" :model="form">
      <el-form-item prop="fttlcodelines" label="影响总行数:" required>
        <el-input
          v-model="form.fttlcodelines"
          placeholder="影响总行数"
        ></el-input>
      </el-form-item>
      <el-form-item prop="fmodifiedlines" label="修改行数:" required>
        <el-input
          v-model="form.fmodifiedlines"
          placeholder="修改行数"
        ></el-input>
      </el-form-item>
      <el-form-item prop="fcomplexity" label="复杂度:" required>
        <el-radio-group v-model="form.fcomplexity">
          <el-radio-button label="0.8"></el-radio-button>
          <el-radio-button label="1.0"></el-radio-button>
          <el-radio-button label="1.2"></el-radio-button>
        </el-radio-group>
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
import {
  updateQaHeadModifyDetail,
  getQaHeadModifyDetail,
} from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      form: {
        id: "",
        fttlcodelines: "",
        fmodifiedlines: "",
        fcomplexity: "",
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
    async handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getQaHeadModifyDetail(id).catch(() => {
        this.$message.error("测试对象修改明细获取异常");
      });

      this.form = resp.data;
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

<style scoped>
.width-sytle {
  width: 90%;
}
</style>
