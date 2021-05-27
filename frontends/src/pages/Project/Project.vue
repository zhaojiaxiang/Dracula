<template>
  <div>
    <div style="margin-top: 10px">
      <el-row>
        <el-col :span="7"
          ><div style="text-align: right; margin-right: 15px">
            <el-form :inline="true" class="demo-form-inline">
              <el-form-item>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="以联络票检索时，不输入条件默认只显示前99条数据"
                  placement="top"
                >
                  <el-switch
                    v-model="switch_value"
                    inactive-text="项目"
                    active-text="联络票(SIR NO)"
                  >
                  </el-switch>
                </el-tooltip>
              </el-form-item>
            </el-form></div
        ></el-col>
        <el-col :span="17"
          ><div style="text-align: left; margin-top: 2px">
            <el-form
              ref="form"
              v-if="is_project_query"
              :inline="true"
              :model="slip_query_form"
              class="demo-form-inline"
            >
              <el-form-item label="联络票号:">
                <el-input v-model="slip_query_form.slip_no"></el-input>
              </el-form-item>
              <el-form-item label="SIR号:">
                <el-input v-model="slip_query_form.sir_no"></el-input>
              </el-form-item>
              <el-form-item label="订单号:">
                <el-input v-model="slip_query_form.order_no"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="onSlipQuery"
                  v-loading.fullscreen.lock="fullscreenLoading"
                  >查询</el-button
                >
              </el-form-item>
            </el-form>
            <el-form
              ref="form"
              v-if="!is_project_query"
              :inline="true"
              :model="form"
              class="demo-form-inline"
            >
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
                    <span
                      style="float: right; color: #8492a6; font-size: 13px"
                      >{{ item.name }}</span
                    >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="订单号:">
                <el-input v-model="form.order_no"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="onQuery"
                  v-loading.fullscreen.lock="fullscreenLoading"
                  >查询</el-button
                >
              </el-form-item>
            </el-form>
          </div></el-col
        >
      </el-row>
    </div>
    <keep-alive>
    <ProjectSlipNoItembyExpand
      v-if="is_project_query"
      ref="ProjectSlipNoItembyExpand"
    ></ProjectSlipNoItembyExpand>
    </keep-alive>
    <keep-alive>
    <ProjectItemGroup
      v-if="!is_project_query"
      ref="ProjectItemGroup"
    ></ProjectItemGroup>
    </keep-alive>
  </div>
</template>

<script>
import ProjectItemGroup from "../Project/components/ProjectItemGroup";
import ProjectSlipNoItembyExpand from "../Project/components/ProjectSlipNoItembyExpand";
import {
  getWorkingOrganization,
  getWorkingProject,
} from "../../services/commonService";
export default {
  components: {
    ProjectItemGroup,
    ProjectSlipNoItembyExpand,
  },
  data() {
    return {
      organization: [],
      project: [],
      fullscreenLoading: false,
      is_project_query: false,
      switch_value: false,
      form: {
        organization_id: "",
        project_code: "",
        order_no: "",
      },
      slip_query_form: {
        slip_no: "",
        sir_no: "",
        order_no: "",
      },
    };
  },
  watch: {
    switch_value(newval) {
      if (newval) {
        this.is_project_query = true;
      } else {
        this.is_project_query = false;
      }
    },
    form: {
      async handler(val) {
        if (val.organization_id) {
          await this.refreshProject(val.organization_id);
        } else {
          await this.refreshProject("");
        }
      },
      deep: true,
    },
  },
  methods: {
    onQuery() {
      this.fullscreenLoading = true;
      this.$refs.ProjectItemGroup.currentPage = 1;
      this.$refs.ProjectItemGroup.getProjectItems(
        this.form.organization_id,
        this.form.project_code,
        this.form.order_no
      );
      this.rememberOperation(this.form)
      this.fullscreenLoading = false;
    },
    onSlipQuery() {
      this.fullscreenLoading = true;
      this.$refs.ProjectSlipNoItembyExpand.getLiaisons(
        this.slip_query_form.slip_no,
        this.slip_query_form.order_no,
        this.slip_query_form.sir_no
      );
      this.rememberOperation(this.slip_query_form)
      this.fullscreenLoading = false;
    },

    rememberOperation(form){
      localStorage.setItem("is_project_query", this.is_project_query)
      localStorage.setItem("switch_value", this.switch_value)
      localStorage.setItem("query_form", JSON.stringify(form))
    },

    async refreshProject(organization_id) {
      var resp_project = await getWorkingProject(organization_id).catch(() => {
        this.$message.error("制番数据获取异常");
        this.fullscreenLoading = false;
        return;
      });

      this.project = resp_project.data;
    },
  },
  created: async function () {
    this.fullscreenLoading = true;
    var resp = await getWorkingOrganization().catch(() => {
      this.$message.error("组织架构数据获取异常");
      this.fullscreenLoading = false;
      return;
    });
    this.organization = resp.data;
    
    await this.refreshProject("");

    // var is_project = localStorage.getItem("is_project_query")

    // var query_form = JSON.parse(localStorage.getItem("query_form"))

    // console.log(query_form);

    // this.is_project_query = !is_project

    // if(is_project){
    //   this.is_project_query = true
    //   // this.switch_value = switch_value_temp
    //   this.form = query_form
    //   this.onQuery()
    // }else{
    //   this.is_project_query = false
    //   // this.switch_value = true
    //   this.slip_query_form = query_form
    //   this.onSlipQuery()
    // }

    this.fullscreenLoading = false;
  },
};
</script>

<style scoped>
.not-display {
  display: none;
}
</style>
