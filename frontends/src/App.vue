<template>
  <div id="app">
    <el-container>
      <el-header>
        <Header />
      </el-header>
      <el-container>
        <el-aside width="4%">
          <Side />
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from "./pages/Home/components/Header";
import Side from "./pages/Home/components/Side";
export default {
  name: "App",
  components: {
    Header,
    Side,
  },
};
</script>

<style scoped>
#app {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  overflow-y: auto;
  background-color: #f0f2f5;
}

.el-header {
  padding: 0px;
  height: 50%;
}
.el-aside {
  overflow: visible;
}
.el-main {
  padding: 0px;
  height: calc(100vh - 60px);
}
</style>
