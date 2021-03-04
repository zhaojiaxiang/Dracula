<template>
  <div class="body-color">
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <el-row>
      <el-col :xs="22" :sm="22" :md="22" :lg="22" :xl="22">
        <Guide>
          <template>
            <div>
              <h5><strong>联络票&单体测试</strong></h5>
            </div>
          </template>
        </Guide>
        <div>
          <ProjectSlipNoItem></ProjectSlipNoItem>
        </div>
        <div>
          <ProjectPclItem></ProjectPclItem>
        </div>
      </el-col>
      <el-col :xs="2" :sm="2" :md="2" :lg="2" :xl="2"
        ><div>
        </div
      ></el-col>
    </el-row>
  </div>
</template>

<script>
import ProjectSlipNoItem  from "./ProjectSlipNoItem";
import ProjectPclItem  from "./ProjectPclItem";
import Guide from "./../../Home/components/Guide";
export default {
  components: {
    ProjectSlipNoItem,
    ProjectPclItem,
    Guide,
  },
  data() {
    return {
      order_no: '',
    };
  },
  methods: {
    goBack() {
      this.$router.push({ name: "Home" }).catch(() => {});
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
