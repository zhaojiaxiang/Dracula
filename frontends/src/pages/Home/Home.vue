<template>
  <div class="body-color">
    <el-row>
      <el-col :xs="22" :sm="22" :md="22" :lg="22" :xl="22"
        ><div>
          <Guide>
            <template>
              <div>
                <h5><strong>我参与的项目</strong></h5>
              </div>
            </template>
          </Guide>
          <ProjectItem ref="ProjectItem"></ProjectItem>
          <Guide>
            <template>
              <div>
                <h5><strong>我参与的任务</strong></h5>
              </div>
            </template>
          </Guide>
          <SlipNoNew
            @click="openSlipNoNew()"
            @refreshHome="refreshHome"
          ></SlipNoNew>
          <SlipNoModify
            @click="openSlipNoModifiy(val)"
            @refreshHome="refreshHome"
          ></SlipNoModify>
          <SlipNoItem
            ref="SlipNoItem"
            @refreshHome="refreshHome"
          ></SlipNoItem></div
      ></el-col>
      <el-col :xs="2" :sm="2" :md="2" :lg="2" :xl="2"
        ><div>
            <MyTaskBar ref="MyTaskBar"></MyTaskBar>
        </div
      ></el-col>
    </el-row>
  </div>
</template>

<script>
import Guide from "./components/Guide";
import ProjectItem from "./components/ProjectItem";
import SlipNoItem from "./components/SlipNoItem";
import SlipNoNew from "./components/SlipNoNew";
import SlipNoModify from "./components/SlipNoModify";
import MyTaskBar from './components/MyTaskBar';
export default {
  name: "Home",
  components: {
    Guide,
    ProjectItem,
    SlipNoItem,
    SlipNoNew,
    SlipNoModify,
    MyTaskBar,
  },
  methods: {
    refreshHome() {
      this.$refs.ProjectItem.refreshProjectItems();
      this.$refs.SlipNoItem.refreshLiaisons();
      this.$refs.MyTaskBar.refreshTaskBar();
    },
  },
};
</script>

<style scoped>
.el-row{
    margin: 0px;
}
</style>
