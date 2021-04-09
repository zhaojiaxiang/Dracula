<template>
  <div class="login-container">
    <el-form
      :model="form"
      :rules="rules"
      status-icon
      ref="form"
      label-position="left"
      label-width="0px"
      class="demo-ruleForm login-page"
    >
      <h3 class="title">登录</h3>
      <el-form-item prop="username">
        <el-input
          type="text"
          v-model="form.username"
          auto-complete="off"
          placeholder="用户名"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          type="password"
          v-model="form.password"
          auto-complete="off"
          placeholder="密码"
        ></el-input>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button
          type="primary"
          style="width:100%;"
          @click="handleSubmit('form')"
          :loading="logining"
          >登录</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { login } from "../../services/userService";
export default {
  data() {
    return {
      logining: false,
      form: {
        username: "",
        password: "",
      },
      rules: {
        username: [
          {
            required: true,
            message: "用户名不可为空",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "密码不可为空", trigger: "blur" },
        ],
      },
      checked: false,
    };
  },
  methods: {
    async handleSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          await login(JSON.stringify(this.form))
            .then((resp) => {
              if (Object.prototype.hasOwnProperty.call(resp.data, 'message')) {
                this.$message.error(resp.data.message);
              }else{
                this.$router.push({ path: "/" });
              }
            })
            .catch(() => {
              this.$message.error("登录异常");
            });
        }
      });
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100%;
}
.login-page {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  margin: 180px auto;
  width: 350px;
  padding: 35px 35px 15px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
}
label.el-checkbox.rememberme {
  margin: 0px 0px 15px;
  text-align: left;
}
</style>
