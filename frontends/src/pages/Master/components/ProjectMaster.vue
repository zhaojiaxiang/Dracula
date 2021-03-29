<template>
  <div>
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <div style="margin-top:15px">
      <el-form ref="form" :inline="true" :rules="rules" :model="form" class="demo-form-inline">
        <el-form-item label="项目代码(制番):">
          <el-input v-model="form.fprojectcd"></el-input>
        </el-form-item>
        <el-form-item label="项目名称:">
          <el-input v-model="form.fprojectnm"></el-input>
        </el-form-item>
        <el-form-item label="项目简称:">
          <el-input v-model="form.fprojectsn"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">新建</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div style="text-align:center; margin-top:15px">
      <el-table :data="tableData" style="width: 50%" v-loading="loading">
        <el-table-column prop="fprojectcd" label="项目代码(制番)" width="180">
        </el-table-column>
        <el-table-column prop="fprojectnm" label="项目名称" width="180">
        </el-table-column>
        <el-table-column prop="fprojectsn" label="项目简称" width="180">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.row.fprojectcd, scope.row.id)"
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
  getProjectMaster,
  newProjectMaster,
  deleteProjectMaster,
} from "./../../../services/master";
export default {
  data() {
    return {
      loading: false,
      tableData: [],
      form: {
        fprojectcd: "",
        fprojectnm: "",
        fprojectsn: "",
        fautoflg: "N",
      },
      rules: {
        fprojectcd: [
          { required: true, message: "请输入项目代码", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    async handleDelete(fprojectcd, id) {
      this.$confirm("此操作将永久删除" + fprojectcd + ", 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            var resp = await deleteProjectMaster(id).catch(() => {
              this.$message.error("项目代码删除异常！");
            });
            if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
              this.refreshProjectList();
              this.$message({
                message: fprojectcd + "已经删除！",
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
          var resp = await newProjectMaster(this.form).catch(() => {
            this.$message.error("项目代码创建异常！");
          });

          if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
            this.refreshProjectList();
            this.$message({
              message: this.form.fprojectcd + "创建成功！",
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
      var resp = await getProjectMaster().catch(() => {
        this.$message.error("项目主表数据获取异常");
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
