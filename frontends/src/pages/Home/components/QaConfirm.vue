<template>
  <el-dialog title="测试结果确认" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item prop="flevel" size="medium" required>
        <el-select v-model="form.flevel" placeholder="请选择难易等级">
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

      <el-form-item prop="freviewcode" size="medium" required>
        <el-input placeholder="确认结果" v-model="form.freviewcode"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button
        id="submitbtn"
        type="primary"
        @click="onSubmit('form')"
        v-loading.fullscreen.lock="fullscreenLoading"
        >确 定</el-button
      >
      <el-button @click="dialogFormVisible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { getQaHead, updateQaHead } from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      qahead: {},
      fullscreenLoading: false,
      form: {
        freviewcode: "",
        flevel: "",
      },
      rules: {
        freviewcode: [
          { required: true, message: "请输入测试结果", trigger: "change" },
        ],
        flevel: [
          { required: true, message: "请选择难易等级", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          this.qahead.flevel = this.form.flevel;
          this.qahead.freviewcode = this.form.freviewcode;
          this.qahead.fstatus = "4";
          var resp = await updateQaHead(this.qahead.id, this.qahead).catch(
            () => {
              this.$message.error("确认异常");
            }
          );
          if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.$message.error(resp.data.message);
            return;
          }
          this.$message.success("确认成功");
          this.dialogFormVisible = !this.dialogFormVisible;
          this.$emit("confirmed");
        }
      });
    },
    async handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      //   this.qaheadid = id;
      var resp = await getQaHead(id).catch(() => {
        this.$message.error("测试数据获取异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
        return;
      }
      this.qahead = resp.data;
      this.form.freviewcode = this.qahead.freviewcode
      this.form.flevel = this.qahead.flevel
    },
  },
};
</script>

<style scoped>
.width-sytle {
  width: 90%;
}
</style>
