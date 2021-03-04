<template>
  <el-dialog title="手动添加结合测试" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item>
        <el-col :span="12">
          <el-form-item prop="fslipno">
            <el-input
              v-model="form.fslipno"
              class="width-sytle"
              placeholder="订单号"
              :disabled="true"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item prop="fobjectid" required>
            <el-input
              v-model="form.fobjectid"
              class="width-sytle"
              placeholder="测试对象"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="onSubmit('form')">确 定</el-button>
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
      qahf_id:"",
      form: {
        fsystemcd: "",
        fprojectcd: "",
        ftesttyp: "PCL",
        fslipno: "",
        fobjectid: "",
        fstatus:"1",
      },
      rules: {
        fobjectid: [
          { required: true, message: "请输入测试对象", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    async handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      this.qahf_id = id;
      var resp = await getQaHead(id).catch(() => {
        this.$message.error("结合测试数据获取异常");
      });
      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      }
      this.form.fsystemcd = resp.data.fsystemcd;
      this.form.fprojectcd = resp.data.fprojectcd;
      this.form.fobjectid = resp.data.fobjectid;
      this.form.fslipno = resp.data.fslipno;
    },

    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await updateQaHead(this.qahf_id, this.form).catch(() => {
            this.$message.error("更新添加结合测试异常");
          });

          if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.$message.error(resp.data.message);
          } else {
            this.dialogFormVisible = false;
            this.$message({
              message: "更新成功！",
              type: "success",
            });
            this.$emit("refreshPCLList");
          }
        }
      });
    },
  },
};
</script>

<style scoped>
.width-sytle {
  width: 90%;
}
</style>
