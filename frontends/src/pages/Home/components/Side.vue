<template>
  <div>
    <el-menu
      default-active="1"
      background-color="#f7f7f7"
      :collapse="isCollapse"
      class="side-height"
    >
    <el-menu-item index="1" @click="push2home">
        <i class="el-icon-menu"></i>
        <span slot="title">工作台</span>
      </el-menu-item>
      <el-menu-item index="2" @click="push2project">
        <i class="el-icon-collection"></i>
        <span slot="title">项目</span>
      </el-menu-item>
      <el-menu-item index="3" v-show="false">
        <i class="el-icon-s-data"></i>
        <span slot="title">统计</span>
      </el-menu-item>
      <el-menu-item index="4" v-show="false">
        <i class="el-icon-user"></i>
        <span slot="title">成员</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isCollapse: true,
    };
  },
  methods:{
    push2home(){
      this.$router.push({ name: "Home" }).catch(() => {});
    },
    push2project(){
      this.$router.push({ name: "Project" }).catch(() => {});
    }
  }
};
</script>

<style scoped>
.side-height{
  height: calc(100vh - 60px);
}
</style>
