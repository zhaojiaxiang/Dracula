<template>
  <div>
    <div style="text-align:center; margin-top:10px">
      <el-form ref="form" :inline="true" :model="form" class="demo-form-inline">
        <el-form-item label="组别:">
          <el-select v-model="form.organization_id" clearable>
            <el-option
              v-for="item in organization"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="制番号:">
          <el-select v-model="form.project_code" clearable>
            <el-option
              v-for="item in project"
              :key="item.keyid"
              :label="item.id"
              :value="item.id"
            >
              <span style="float: left">{{ item.id }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{
                item.name
              }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单号:">
          <el-input v-model="form.order_no"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQuery" v-loading.fullscreen.lock="fullscreenLoading">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <ProjectItemGroup ref="ProjectItemGroup"></ProjectItemGroup>
  </div>
</template>

<script>
import ProjectItemGroup from "../Project/components/ProjectItemGroup";
import {
  getWorkingOrganization,
  getWorkingProject,
} from "../../services/commonService";
export default {
  components: {
    ProjectItemGroup,
  },
  data() {
    return {
      organization: [],
      project: [],
      fullscreenLoading: false,
      form: {
        organization_id: "",
        project_code: "",
        order_no: "",
      },
    };
  },
  watch: {
    form: {
      async handler(val) {
        if (val.organization_id) {
          await this.refreshProject(val.organization_id);
        }else{
          await this.refreshProject("");
        }
      },
      deep: true,
    },
  },
  methods: {
    onQuery() {
      this.fullscreenLoading = true
      this.$refs.ProjectItemGroup.currentPage = 1
      this.$refs.ProjectItemGroup.getProjectItems(
        this.form.organization_id,
        this.form.project_code,
        this.form.order_no
      );
      this.fullscreenLoading = false
    },
    async refreshProject(organization_id) {
      var resp_project = await getWorkingProject(organization_id).catch(() => {
        this.$message.error("制番数据获取异常");
        this.fullscreenLoading = false
        return;
      });

      this.project = resp_project.data;
    },
  },
  created: async function() {
    this.fullscreenLoading = true
    var resp = await getWorkingOrganization().catch(() => {
      this.$message.error("组织架构数据获取异常");
      this.fullscreenLoading = false
      return;
    });
    this.organization = resp.data;

    await this.refreshProject("");
    this.fullscreenLoading = false
  },
};
</script>

<style></style>
