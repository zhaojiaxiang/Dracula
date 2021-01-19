<template>
  <el-dialog title="测试对象修改概要" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item prop="fobjmodification" required>
        <el-input
          type="textarea"
          :rows="10"
          placeholder="请输入修改概要"
          v-model="form.fobjmodification"
        >
        </el-input>
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
import { getQaHead, updateQaHeadSummary } from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      form: {
        id: "",
        fobjmodification: "",
      },
      rules: {
        fobjmodification: [
          { required: true, message: "请输入修改概要", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    async handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getQaHead(id).catch(() => {
        this.$message.error("测试对象数据获取异常");
        return;
      });
      if (resp.status === 200) {
        this.form = resp.data;
      }
    },
    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await updateQaHeadSummary(this.form.id, this.form).catch(
            () => {
              this.$message.error("测试项修改概要更新异常");
            }
          );
          if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.dialogFormVisible = false;
            this.resetForm("form");
            this.$message({
              message: this.form.fobjectid + "修改概要更新成功！",
              type: "success",
            });
          } else {
            this.$message.error(resp.data.message);
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
