<template>
  <div class="div_style">
    <Guide>
      <template>
        <div style="text-align:center">
          <h5><strong>我的待办</strong></h5>
        </div>
      </template>
    </Guide>
    <el-row>
      <el-col>
        <el-card shadow="hover" class="task-card-color">
          <div @click="testing()">
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  <h6 class="clear-margin-padding">
                    {{ taskbar.testing }}
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  测试中
                </div></el-col
              >
            </el-row>
          </div>
        </el-card>
        <el-card shadow="hover" class="task-card-color">
          <div @click="approval()">
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  <h6 class="clear-margin-padding">
                    {{ taskbar.approval }}
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  待审核
                </div></el-col
              >
            </el-row>
          </div>
        </el-card>
        <el-card shadow="hover" class="task-card-color">
          <div @click="confirm()">
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  <h6 class="clear-margin-padding">
                    {{ taskbar.confirm }}
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  待确认
                </div></el-col
              >
            </el-row>
          </div>
        </el-card>
        <el-card shadow="hover" class="task-card-color">
          <div @click="release()">
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  <h6 class="clear-margin-padding">
                    {{ taskbar.release }}
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div style="text-align:center">
                  待发布
                </div></el-col
              >
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Guide from "./Guide";
import { getMyTaskBar } from "./../../../services/liaisonService";
export default {
  components:{
    Guide
  },
  data() {
    return {
      taskbar: {},
    };
  },
  methods: {
    testing() {
      this.$router.push({ name: "Task", query: { type: 'testing' } });
    },
    approval() {
      this.$router.push({ name: "Task", query: { type: 'approval' } });
    },
    confirm() {
      this.$router.push({ name: "Task", query: { type: 'confirm' } });
    },
    release() {
      this.$router.push({ name: "Task", query: { type: 'release' } });
    },
    async refreshTaskBar() {
      var resp = await getMyTaskBar().catch(() => {
        this.$message.error("任务栏数据获取异常");
      });

      this.taskbar = resp.data[0];
    },
  },
  mounted: function() {
    this.refreshTaskBar();
  },
};
</script>

<style scoped>
.div_style {
  overflow: visible;
  background: #f7f7f7;
  padding: 6px;
  height: calc(100vh - 60px);
  border-left: 1px solid #dce3e8;
}
.task-card-color {
  background: #f7f7f7;
  margin-bottom: 5px;
}
</style>
