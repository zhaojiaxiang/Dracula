<template>
  <div class="body-color">
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <el-row>
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <div>
          <ProjectSlipNoItem></ProjectSlipNoItem>
        </div>
        <div>
          <ProjectPclItem></ProjectPclItem>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import ProjectSlipNoItem  from "./ProjectSlipNoItem";
import ProjectPclItem  from "./ProjectPclItem";
export default {
  components: {
    ProjectSlipNoItem,
    ProjectPclItem,
  },
  data() {
    return {
      order_no: '',
    };
  },
  methods: {
    goBack() {
      //返回上一个路由
      this.$router.go(-1)
    },
  },
  mounted:function(){
    this.order_no = this.$route.query.order_no;
  }
};
</script>

<style scoped>
.el-row {
  margin: 0px;
}
.project_header {
  height: 100px;
  background-color: darkgray;
}
</style>
