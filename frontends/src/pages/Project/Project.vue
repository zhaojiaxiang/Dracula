<template>
  <div>
    <div style="text-align:center; margin-top:15px">
      <el-form ref="form" :inline="true" :model="form" class="demo-form-inline">
        <el-form-item label="制番号:">
          <el-input v-model="form.project_code"></el-input>
        </el-form-item>
        <el-form-item label="订单号:">
          <el-input v-model="form.order_no"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQuery">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <ProjectItemGroup ref="ProjectItemGroup"></ProjectItemGroup>
  </div>
</template>

<script>
import ProjectItemGroup from "../Project/components/ProjectItemGroup";
export default {
  components: {
    ProjectItemGroup,
  },
  data() {
    return {
      form: {
        project_code: "",
        order_no: "",
      },
    };
  },
  methods: {
    onQuery() {
      this.$refs.ProjectItemGroup.getProjectItems(
        this.form.project_code,
        this.form.order_no
      );
    },
  },
};
</script>

<style></style>
