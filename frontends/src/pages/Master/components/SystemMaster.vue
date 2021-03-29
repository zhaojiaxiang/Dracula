<template>
  <div>
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <div style="margin-top:15px">
      <el-form
        ref="form"
        :inline="true"
        :rules="rules"
        :model="form"
        class="demo-form-inline"
      >
        <el-form-item label="系统代码:" required>
          <el-input v-model="form.fsystemcd"></el-input>
        </el-form-item>
        <el-form-item label="系统名称:">
          <el-input v-model="form.fsystemnm"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">新建</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div style="text-align:center; margin-top:15px">
      <el-table :data="tableData" style="width: 50%" v-loading="loading">
        <el-table-column prop="fsystemcd" label="系统代码" width="180">
        </el-table-column>
        <el-table-column prop="fsystemnm" label="系统名称" width="180">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.row.fsystemcd, scope.row.id)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import {
  getSystemMaster,
  newSystemMaster,
  deleteSystemMaster,
} from "./../../../services/master";
export default {
  data() {
    return {
      loading: false,
      tableData: [],
      form: {
        fsystemcd: "",
        fsystemnm: "",
      },
      rules: {
        fsystemcd: [
          { required: true, message: "请输入系统代码", trigger: "change" },
        ],
        fsystemnm: [
          { required: true, message: "请输入系统名称", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    async handleDelete(fsystemcd, id) {
      this.$confirm("此操作将永久删除" + fsystemcd + ", 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            var resp = await deleteSystemMaster(id).catch(() => {
              this.$message.error("系统代码删除异常！");
            });
            if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
              this.refreshProjectList();
              this.$message({
                message: fsystemcd + "已经删除！",
                type: "success",
              });
            } else {
              this.$message.error(resp.data.message);
            }
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },
    onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await newSystemMaster(this.form).catch(() => {
            this.$message.error("系统代码创建异常！");
          });

          if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.refreshProjectList();
            this.$message({
              message: this.form.fsystemcd + "创建成功！",
              type: "success",
            });
          } else {
            this.$message.error(resp.data.message);
          }
        }
      });
    },

    goBack() {
      //返回上一个路由
      this.$router.go(-1)
    },

    async refreshProjectList() {
      this.loading = true;
      var resp = await getSystemMaster().catch(() => {
        this.$message.error("系统主表数据获取异常");
        this.loading = false;
        return;
      });
      this.tableData = resp.data;
      this.loading = false;
    },
  },
  created: function() {
    this.refreshProjectList();
  },
};
</script>

<style></style>
