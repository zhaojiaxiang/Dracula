<template>
  <div style="margin: 30px">
    <el-row :gutter="50">
      <el-col :span="5">
        <el-card>
          <div slot="header" class="clearfix">
            <span>个人信息</span>
          </div>
          <div style="text-align: center">
            <el-avatar :size="150" :src="userInfo.avatar"></el-avatar>
          </div>
          <el-divider content-position="left">上传头像</el-divider>
          <div style="text-align: center">
            <el-upload
                ref="upload"
              class="avatar-uploader"
              action="/api/file_upload/"
              :before-upload="beforeFileUpload"
              accept="image/*"
              :on-success="refreshFileList"
              :limit="1"
            >
              
              <i class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-tabs type="border-card">
          <el-tab-pane label="个人信息">
            <el-form :model="userInfo" label-width="100px" style="width: 50%">
              <el-form-item label="用户名:">
                <el-input
                  :disabled="true"
                  v-model="userInfo.username"
                ></el-input>
              </el-form-item>
              <el-form-item label="中文名:">
                <el-input :disabled="true" v-model="userInfo.name"></el-input>
              </el-form-item>
              <el-form-item label="邮箱:">
                <el-input :disabled="true" v-model="userInfo.email"></el-input>
              </el-form-item>
              <el-form-item label="SLIMS名:">
                <el-input
                  :disabled="true"
                  v-model="userInfo.slmsname"
                ></el-input>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="密码修改">
            <el-form
              :model="ruleForm"
              :rules="rules"
              ref="ruleForm"
              label-width="100px"
              style="width: 50%"
            >
              <el-form-item
                label="旧密码："
                prop="password"
                :error="errorinfo.password"
              >
                <el-input
                  type="password"
                  v-model="ruleForm.password"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="密码：" prop="newpassword1">
                <el-input
                  type="password"
                  v-model="ruleForm.newpassword1"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item label="确认密码：" prop="newpassword2">
                <el-input
                  type="password"
                  v-model="ruleForm.newpassword2"
                  autocomplete="off"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="submitPasswordForm('ruleForm')"
                  >确认修改</el-button
                >
                <el-button @click="resetForm('ruleForm')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="工时系统">
            <el-form label-width="100px" style="width: 50%">
              <el-form-item label="同步日期：">
                <el-checkbox-group v-model="weeksGroup" size="medium">
                  <el-checkbox-button
                    v-for="week in weeks"
                    :label="week"
                    :key="week"
                    >{{ week }}</el-checkbox-button
                  >
                </el-checkbox-group>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitManPower"
                  >确认修改</el-button
                >
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const weeksOption = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];
import {
  updateUserPassword,
  updateEmailDays,
  getUserInfo,
  updateAvatar,
} from "./../../services/userService";
import { removeToken } from "@/utils/auth";
export default {
  data() {
    var validateOldPass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入旧密码"));
      } else {
        callback();
      }
    };
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("newpassword2");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.newpassword1) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        password: "",
        newpassword1: "",
        newpassword2: "",
      },
      errorinfo: {
        password: "",
      },
      userInfo: {},
      weeks: weeksOption,
      emaildays: "",
      weeksGroup: [],
      avatarlist:[],

      rules: {
        password: [{ validator: validateOldPass, trigger: "blur" }],
        newpassword1: [{ validator: validatePass, trigger: "blur" }],
        newpassword2: [{ validator: validatePass2, trigger: "blur" }],
      },
    };
  },
  methods: {
    submitPasswordForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var passwordInfo = {
            password: this.ruleForm.password,
            new_password: this.ruleForm.newpassword1,
          };
          var resp = await updateUserPassword(passwordInfo).catch(() => {
            this.$message.error("密码修改异常！");
          });
          if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.errorinfo.password = resp.data.message;
          } else {
            this.$alert("密码修改成功，请重新登录系统", "", {
              confirmButtonText: "确定",
              callback: () => {
                this.logout();
              },
            });
          }
        } else {
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    async refreshUserInfo() {
      var resp = await getUserInfo(this.userInfo.id).catch(() => {
        this.$message.error("用户数据信息获取异常！");
      });

      this.userInfo = resp.data;
      localStorage.setItem("UserInfo", JSON.stringify(this.userInfo));
    },

    refreshManPower() {
      this.userInfo = JSON.parse(localStorage.getItem("UserInfo"));
      this.emaildays = this.userInfo.fmaildays;
      this.emaildays = this.emaildays.replace("1", "周一");
      this.emaildays = this.emaildays.replace("2", "周二");
      this.emaildays = this.emaildays.replace("3", "周三");
      this.emaildays = this.emaildays.replace("4", "周四");
      this.emaildays = this.emaildays.replace("5", "周五");
      this.emaildays = this.emaildays.replace("6", "周六");
      this.emaildays = this.emaildays.replace("7", "周日");
      this.weeksGroup = this.emaildays.split(",");
    },

    async submitManPower() {
      this.weeksGroup.sort();
      var weekGroupStr = this.weeksGroup.join(",");
      weekGroupStr = weekGroupStr.replace("周一", "1");
      weekGroupStr = weekGroupStr.replace("周二", "2");
      weekGroupStr = weekGroupStr.replace("周三", "3");
      weekGroupStr = weekGroupStr.replace("周四", "4");
      weekGroupStr = weekGroupStr.replace("周五", "5");
      weekGroupStr = weekGroupStr.replace("周六", "6");
      weekGroupStr = weekGroupStr.replace("周日", "7");

      await updateEmailDays(weekGroupStr).catch(() => {
        this.$message.error("工时系统信息修改异常！");
      });

      this.$message.success("工时系统信息修改成功！");
      await this.refreshUserInfo();
      this.refreshManPower();
    },

    logout: function () {
      removeToken();
      window.location.reload();
    },

    async beforeFileUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;

      let fileForm = new FormData();

      if (!isLt2M) {
        this.$message.error("上传文件大小不能超过 2MB!");
      }

      fileForm.append("avatar", file);

      await updateAvatar(fileForm).catch(()=>{
          this.$message.error("头像上传异常！");
      })

      await this.refreshUserInfo();
      this.bus.$emit("login_succ");

    },

    refreshFileList(){
       this.$refs.upload.clearFiles()
    },
  },
  mounted() {
    this.refreshManPower();
  },
};
</script>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>