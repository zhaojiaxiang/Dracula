<template>
  <div>
    <el-drawer
      class="drawer-height"
      :visible.sync="drawer"
      :with-header="false"
      size="50%"
    >
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="10%"
        size="medium"
        style="width: 95%; margin-top:20px;"
        v-loading="loading"
      >
        <el-form-item
          size="medium"
          required
          v-show="true ? form.fstatus == '1' : form.fstatus != '1'"
        >
          <el-col :span="8">
            <el-form-item prop="fsystemcd" class="width-sytle" size="medium">
              <el-select
                v-model="form.fsystemcd"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请选择系统名称"
              >
                <el-option
                  v-for="(item, i) in systems"
                  :key="i"
                  :label="item.fsystemcd"
                  :value="item.fsystemcd"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="fprojectcd" class="width-sytle" size="medium">
              <el-select
                v-model="form.fprojectcd"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请选择项目名称"
              >
                <el-option
                  v-for="(item, i) in projects"
                  :key="i"
                  :label="projects.fprojectcd"
                  :value="item.fprojectcd"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="ftype" size="medium">
              <el-select
                v-model="form.ftype"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请选择开发类型"
              >
                <el-option label="追加开发" value="追加开发"></el-option>
                <el-option label="改善需求" value="改善需求"></el-option>
                <el-option
                  label="维护阶段障碍"
                  value="维护阶段障碍"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item size="medium" required>
          <el-col :span="8">
            <el-form-item prop="fassignedto" class="width-sytle" size="medium">
              <el-select
                v-model="form.fassignedto"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请选择对应者"
              >
                <el-option
                  v-for="(item, i) in groupusers"
                  :key="i"
                  :v-label="item.name"
                  :value="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="fleader" size="medium" class="width-sytle" required>
              <el-select
                v-model="form.fleader"
                multiple
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请选择负责人"
              >
                <el-option
                  v-for="(item, i) in groupusers"
                  :key="i"
                  :v-label="item.name"
                  :value="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item size="medium">
              <el-select
                multiple
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                v-model="form.fhelper"
                placeholder="请选择项目协助者"
              >
                <el-option-group
                  v-for="group in allusers"
                  :key="group.label"
                  :label="group.label"
                >
                  <el-option
                    v-for="item in group.options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-option-group>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item size="medium" required>
          <el-col :span="8">
            <el-form-item prop="fslipno" size="medium">
              <el-input
                v-model="form.fslipno"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                class="width-sytle"
                placeholder="请输入联络票号"
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item prop="fodrno" size="medium">
              <el-input
                v-model="form.fodrno"
                class="width-sytle"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="请输入订单号"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item size="medium">
              <el-input
                disabled
                v-model="form.fsirno"
                placeholder="SIR No"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item prop="fbrief" size="medium">
          <el-input
            type="textarea"
            :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
            v-model="form.fbrief"
            placeholder="开发概要"
          ></el-input>
        </el-form-item>
        <el-form-item prop="fcontent" size="medium">
          <el-input
            type="textarea"
            :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
            v-model="form.fcontent"
            placeholder="问题描述"
          ></el-input>
        </el-form-item>
        <el-form-item size="medium">
          <el-input
            type="textarea"
            :disabled="true ? form.fstatus == '5' : form.fstatus != '5'"
            v-model="form.fanalyse"
            placeholder="问题分析"
          ></el-input>
        </el-form-item>
        <el-form-item size="medium">
          <el-input
            type="textarea"
            :disabled="true ? form.fstatus == '5' : form.fstatus != '5'"
            v-model="form.fsolution"
            placeholder="解决方案"
          ></el-input>
        </el-form-item>
        <el-form-item
          required
          v-show="true ? form.fstatus == '1' : form.fstatus == '1'"
        >
          <el-col :span="8">
            <el-form-item prop="fplnstart">
              <el-date-picker
                type="date"
                size="medium"
                value-format="yyyy-MM-dd"
                placeholder="计划开始日期"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                v-model="form.fplnstart"
                class="width-sytle"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="fplnend">
              <el-date-picker
                type="date"
                size="medium"
                value-format="yyyy-MM-dd"
                placeholder="计划结束日期"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                v-model="form.fplnend"
                class="width-sytle"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item size="medium">
              <el-input
                v-model="form.fplnmanpower"
                :disabled="true ? form.fstatus != '1' : form.fstatus == '1'"
                placeholder="计划工时"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item
          required
          v-show="true ? form.fstatus != '1' : form.fstatus != '1'"
        >
          <el-col :span="3">
            <el-form-item size="medium">
              <el-upload
                class="upload-demo"
                action="/api/file_upload/"
                :before-upload="beforeFileUpload"
                :limit="1"
              >
                <el-link
                  :disabled="isCanUpload()"
                  :underline="false"
                  icon="el-icon-upload2"
                  >上传</el-link
                >
              </el-upload>
            </el-form-item>
          </el-col>
          <el-col :span="3">
            <el-form-item size="medium">
              <el-link
                :underline="false"
                :disabled="isCanDownload()"
                icon="el-icon-download"
                :href="form.freleaserpt"
                >下载</el-link
              >
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item size="medium">
              <el-input
                :disabled="true ? form.fstatus != '2' : form.fstatus == '2'"
                v-model="form.fplnmanpower"
                style="width:80%"
                placeholder="计划工时"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item size="medium">
              <el-input
                :disabled="true ? form.fstatus != '2' : form.fstatus == '2'"
                v-model="form.factmanpower"
                style="width:80%"
                placeholder="实际工时"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :disabled="true ? form.fstatus == '4' : form.fstatus != '4'" @click="onSubmit('form')">更新</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script>
import {
  getSingleLiaison,
  modifyLiaison,
} from "../../../services/liaisonService";
import { handleAllUser } from "../../../static/js/commonJs";
import {
  getProjects,
  getSystems,
  getGroupUsers,
  getAllUsers,
} from "../../../services/commonService";
import { liaisonfileUpdate } from "../../../services/liaisonService";
export default {
  data() {
    return {
      loading:false,
      drawer: false,
      projects: {},
      systems: {},
      groupusers: {},
      allusers: [],
      form: {
        id: "",
        fsystemcd: "",
        fprojectcd: "",
        fslipno: "",
        ftype: "",
        fstatus: "",
        fodrno: "",
        fassignedto: "",
        fhelper: "",
        fleader: "",
        fbrief: "",
        fcontent: "",
        fanalyse: "",
        fsolution: "",
        fplnstart: "",
        fplnend: "",
        factstart: "",
        factend: "",
        fsirno: "",
        fplnmanpower: 0,
        factmanpower: 0,
        freleaserpt: "",
      },
      rules: {
        fsystemcd: [
          { required: true, message: "请输入系统名称", trigger: "blur" },
        ],
        fprojectcd: [
          { required: true, message: "请选择项目名称", trigger: "change" },
        ],
        fassignedto: [
          { required: true, message: "请选择对应者", trigger: "change" },
        ],
        fleader: [
          { required: true, message: "请选择负责人", trigger: "change" },
        ],
        fplnstart: [
          {
            required: true,
            message: "请选择日期",
            trigger: "change",
          },
        ],
        fplnend: [
          {
            required: true,
            message: "请选择日期",
            trigger: "change",
          },
        ],
        ftype: [
          {
            required: true,
            message: "请至少选择一个开发类型",
            trigger: "change",
          },
        ],
        fodrno: [{ required: true, message: "请输入订单", trigger: "change" }],
        fslipno: [
          { required: true, message: "请输入联络票号", trigger: "change" },
        ],
        fbrief: [
          { required: true, message: "请输入开发概要", trigger: "blur" },
        ],
        fcontent: [
          { required: true, message: "请输入问题描述", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var fleader_arr = this.form.fleader;


          if (fleader_arr) {
            this.form.fleader = fleader_arr.join(",");
          } else {
            this.form.fleader = "";
          }

          var fhelper_arr = this.form.fhelper;
          if (fhelper_arr) {
            this.form.fhelper = fhelper_arr.join(",");
          } else {
            this.form.fhelper = "";
          }

          var resp = await modifyLiaison(this.form.id, this.form);
          if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.$emit("refreshHome");
            this.$message({
              message: this.form.fslipno + "更新成功！",
              type: "success",
            });
            this.drawer = false;
          } else {
            this.$message.error(this.form.fslipno + resp.data.message);
            this.form.fleader = this.form.fleader.split(",");
            this.form.fhelper = this.form.fhelper.split(",");
          }
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    isCanDownload() {
      if (this.form.freleaserpt) {
        return false;
      }
      return true;
    },

    isCanUpload() {
      if (this.form.fstatus === "3") {
        return false;
      }
      return true;
    },

    async beforeFileUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;

      let fileForm = new FormData();

      if (!isLt2M) {
        this.$message.error("上传文件大小不能超过 2MB!");
      }

      fileForm.append("file", file);
      fileForm.append("liaison", this.form.id);

      var resp = await liaisonfileUpdate(fileForm).catch(() => {
        this.$message.error("文件上传到服务器异常");
      });

      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("文件上传成功");
        var resp_l = await getSingleLiaison(this.form.id).catch(() => {
          this.$message.error("联络票数据获取异常");
          return;
        });
        this.form = resp_l.data;
        this.form.freleaserpt = "media/upload/file/" + this.form.freleaserpt
      }
    },
  },
  mounted: function() {
    this.loading = true;
    var this_ = this;
    this.bus.$on("openSlipNoModifiy", async function(id) {
      this_.drawer = true;
      var p_resp = await getProjects().catch(() => {
        this.$message.error("项目主表数据获取异常");
        this.loading = false;
        return;
      });
      var s_resp = await getSystems().catch(() => {
        this.$message.error("系统主表数据获取异常");
        this.loading = false;
        return;
      });
      var g_resp = await getGroupUsers().catch(() => {
        this.$message.error("分组用户主表数据获取异常");
        this.loading = false;
        return;
      });
      var u_resp = await getAllUsers().catch(() => {
        this.$message.error("用户主表数据获取异常");
        this.loading = false;
        return;
      });
      var resp = await getSingleLiaison(id).catch(() => {
        this.$message.error("联络票数据获取异常");
        this.loading = false;
        return;
      });

      var liaison = resp.data;
      if (liaison.fhelper) {
        liaison.fhelper = liaison.fhelper.split(",");
      } else {
        liaison.fhelper = [];
      }

      if (liaison.fleader) {
        liaison.fleader = liaison.fleader.split(",");
      } else {
        liaison.fleader = [];
      }
      this_.form = resp.data;
      if(this_.form.freleaserpt){
        this_.form.freleaserpt = "media/upload/file/" + this_.form.freleaserpt
      }

      this_.projects = p_resp.data;
      this_.systems = s_resp.data;
      this_.groupusers = g_resp.data;
      var usersjson = u_resp.data;
      this_.allusers = handleAllUser(usersjson);
    });
    this.loading = false;
  },
};
</script>

<style scoped>
.drawer-height {
  height: calc(100vh);
  overflow: visible;
}
.width-sytle {
  width: 90%;
}
</style>
