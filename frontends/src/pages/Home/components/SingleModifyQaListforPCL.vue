<template>
  <el-dialog title="修改测试用例" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item prop="fcontent" required>
        <el-input v-model="form.fcontent" placeholder="测试用例"></el-input>
      </el-form-item>
      <el-form-item>
        <el-col :span="9">
          <el-form-item prop="fclass1" required>
            <el-input
              v-model="form.fclass1"
              class="width-sytle"
              placeholder="分类1"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="9">
          <el-form-item prop="fclass2" required>
            <el-input
              v-model="form.fclass2"
              class="width-sytle"
              placeholder="分类2"
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
import { updateQaDetail, getQaDetail } from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      form: {
        id: "",
        fclass1: "",
        fclass2: "",
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
        fclass1: [{ required: true, message:"请输入分类1", trigger:"change" }],
        fclass2: [{ required: true, message:"请输入分类2", trigger:"change" }],
        fsortrule: [{ required: false }],
      },
    };
  },
  methods: {
    async handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getQaDetail(id);
      this.form = resp.data;
    },
    async onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await updateQaDetail(this.form.id, this.form);
          if (resp.status === 200) {
            this.$emit("refreshQaList");
            this.dialogFormVisible = false;
            this.resetForm("form");
            this.$message({
              message: this.form.fcontent + "修改成功！",
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
