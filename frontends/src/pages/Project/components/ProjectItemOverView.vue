<template>
  <div class="body-color">
    <el-row>
      <el-col :xs="22" :sm="22" :md="22" :lg="22" :xl="22">
        <div>
          <ProjectSlipNoItem></ProjectSlipNoItem>
        </div>
      </el-col>
      <el-col :xs="2" :sm="2" :md="2" :lg="2" :xl="2"
        ><div>
          <MyTaskBar></MyTaskBar></div
      ></el-col>
    </el-row>
  </div>
</template>

<script>
import ProjectSlipNoItem  from "./ProjectSlipNoItem";
import MyTaskBar from "./../../Home/components/MyTaskBar";
export default {
  components: {
    MyTaskBar,
    ProjectSlipNoItem
  },
  data() {
    return {
      order_no: '',
    };
  },
  methods: {
    
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
