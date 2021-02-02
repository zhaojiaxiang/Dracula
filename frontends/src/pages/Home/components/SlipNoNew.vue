<template>
  <div>
    <el-drawer class="drawer-height" :visible.sync="drawer" size="55%">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="30%"
        size="medium"
        style="width: 95%;"
        v-loading="loading"
      >
        <el-form-item label="系统名称" size="medium" required>
          <el-col :span="10">
            <el-form-item prop="fsystemcd" size="medium">
              <el-select v-model="form.fsystemcd" placeholder="请选择系统名称">
                <el-option
                  v-for="(item, i) in systems"
                  :key="i"
                  :label="item.fsystemnm"
                  :value="item.fsystemcd"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="14">
            <el-form-item label="项目名称" prop="fprojectcd" size="medium">
              <el-select v-model="form.fprojectcd" placeholder="请选择项目名称">
                <el-option
                  v-for="(item, i) in projects"
                  :key="i"
                  :label="projects.fprojectsn"
                  :value="item.fprojectcd"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="开发类型" size="medium" required>
          <el-col :span="10">
            <el-form-item prop="ftype" size="medium">
              <el-select v-model="form.ftype" placeholder="请选择开发类型">
                <el-option label="追加开发" value="追加开发"></el-option>
                <el-option label="改善需求" value="改善需求"></el-option>
                <el-option
                  label="维护阶段障碍"
                  value="维护阶段障碍"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="14">
            <el-form-item label="对应者" prop="fassignedto" size="medium">
              <el-select v-model="form.fassignedto" placeholder="请选择对应者">
                <el-option
                  v-for="(item, i) in groupusers"
                  :key="i"
                  :v-label="item.name"
                  :value="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="联络票号" size="medium" required>
          <el-col :span="10">
            <el-form-item prop="fslipno" size="medium">
              <el-input
                v-model="form.fslipno"
                placeholder="请输入联络票号"
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col :span="14">
            <el-form-item label="订单号" prop="fodrno" size="medium">
              <el-input
                v-model="form.fodrno"
                placeholder="请输入订单号"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="负责人" size="medium" required>
          <el-col :span="10">
            <el-form-item size="medium">
              <el-select
                v-model="form.fleader"
                multiple
                placeholder="请选择项目负责人"
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
          <el-col :span="14">
            <el-form-item label="协助者" size="medium">
              <el-select
                v-model="form.fhelper"
                multiple
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
        <el-form-item label="开发概要" prop="fbrief" size="medium">
          <el-input type="textarea" v-model="form.fbrief"></el-input>
        </el-form-item>
        <el-form-item label="问题描述" prop="fcontent" size="medium">
          <el-input type="textarea" v-model="form.fcontent"></el-input>
        </el-form-item>
        <el-form-item label="计划开始" required>
          <el-col :span="7">
            <el-form-item prop="fplnstart">
              <el-date-picker
                type="date"
                size="medium"
                value-format="yyyy-MM-dd"
                placeholder="计划开始日期"
                v-model="form.fplnstart"
                style="width:95%"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="13">
            <el-form-item prop="fplnend" label="计划结束">
              <el-date-picker
                type="date"
                size="medium"
                placeholder="计划结束日期"
                value-format="yyyy-MM-dd"
                v-model="form.fplnend"
                style="width:90%"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item size="medium">
              <el-input
                v-model="form.fplnmanpower"
                placeholder="计划工时"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')"
            >立即创建</el-button
          >
          <el-button @click="resetForm('form')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script>
import { newLiaison } from "../../../services/liaisonService";
import {
  getProjects,
  getSystems,
  getAllUsers,
  getGroupUsers,
} from "../../../services/commonService";
import { handleAllUser } from "../../../static/js/commonJs";
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
        fsystemcd: "",
        fprojectcd: "",
        fslipno: "",
        ftype: "",
        fodrno: "",
        fassignedto: "",
        fhelper: "",
        fleader: "",
        fbrief: "",
        fcontent: "",
        fplnstart: "",
        fplnend: "",
        factstart: null,
        factend: null,
        freleasedt: null,
        fplnmanpower: null,
        factmanpower: null,
        freleaserpt: null,
        fsirno: "",
        fgroups: "1",
      },
      rules: {
        fsystemcd: [
          { required: true, message: "请输入系统名称", trigger: "change" },
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
          { required: true, message: "请输入开发概要", trigger: "change" },
        ],
        fcontent: [
          { required: true, message: "请输入问题描述", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    onSubmit(formName) {
      this.loading = true;
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          if (this.form.fleader.length === 0) {
            this.form.fleader = "";
          } else {
            this.form.fleader = this.form.fleader.join(",");
          }

          if (this.form.fhelper.length === 0) {
            this.form.fhelper = "";
          } else {
            this.form.fhelper = this.form.fhelper.join(",");
          }

          var resp = await newLiaison(this.form);

          if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.$emit("refreshHome");
            this.$message({
              message: this.form.fslipno + "创建成功！",
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
      this.loading = false
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
  mounted: function() {
    var this_ = this;
    this_.loading = true
    this.bus.$on("openSlipNoNew", async function() {
      this_.drawer = true;

      var p_resp = await getProjects().catch(() => {
        this.$message.error("项目主表数据获取异常");
        this_.loading = false
        return;
      });
      var s_resp = await getSystems().catch(() => {
        this.$message.error("系统主表数据获取异常");
        this_.loading = false
        return;
      });
      var g_resp = await getGroupUsers().catch(() => {
        this.$message.error("分组用户主表数据获取异常");
        this_.loading = false
        return;
      });
      var u_resp = await getAllUsers().catch(() => {
        this.$message.error("用户主表数据获取异常");
        this_.loading = false
        return;
      });

      this_.projects = p_resp.data;
      this_.systems = s_resp.data;
      this_.groupusers = g_resp.data;
      var usersjson = u_resp.data;
      this_.allusers = handleAllUser(usersjson);
    });
    this_.loading = false
  },
};
</script>

<style scoped>
.drawer-height {
  height: calc(100vh);
  overflow: visible;
}
</style>
