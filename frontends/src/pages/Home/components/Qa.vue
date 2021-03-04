<template>
  <div>
    <el-breadcrumb
      separator-class="el-icon-arrow-right"
      style="font-size:16px; margin-top: 5px;"
    >
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>QA</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row :gutter="10">
      <el-col :xs="2" :sm="3" :md="3" :lg="4" :xl="4"><div></div></el-col>
      <el-col :xs="20" :sm="18" :md="18" :lg="16" :xl="16"
        ><div>
          <el-form
            ref="form"
            :model="form"
            :rules="rules"
            style=" margin-top:20px;"
          >
            <el-form-item>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="form.fsystemcd" disabled></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="form.fprojectcd" disabled></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="liaison.fsirno" disabled></el-input>
                </el-form-item>
              </el-col>
            </el-form-item>
            <el-form-item>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="form.fslipno" disabled></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item prop="fobjectid" required>
                  <el-input
                    v-model="form.fobjectid"
                    placeholder="请填写测试对象名称"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item>
                  <el-button
                    type="primary"
                    @click="onSubmit('form')"
                    :disabled="liaison.fstatus !== '2'"
                    >立即创建</el-button
                  >
                  <el-button type="text" @click="addDesignReview(form.fslipno)"
                    >设计Review</el-button
                  >
                </el-form-item>
              </el-col>
            </el-form-item>
          </el-form>

          <el-table
            :data="qaheads"
            border
            height="420"
            style="margin-top:20px"
            size="medium"
            v-loading="loading"
          >
            <el-table-column
              fixed
              prop="fobjectid"
              label="测试对象"
              width="400"
            >
            </el-table-column>
            <el-table-column prop="fstatus" label="状态" width="130">
              <template slot-scope="scope">
                <el-tag :type="scope.row.tagtype" disable-transitions>{{
                  scope.row.fstatus
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="ftesttyp" label="测试类型" width="120">
            </el-table-column>

            <el-table-column prop="ftestdte" label="测试日期" width="150">
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="250">
              <template slot-scope="scope">
                <el-link
                  type="text"
                  size="medium"
                  :underline="false"
                  @click="addObjectSummary(scope.row.id)"
                  >概要</el-link
                >
                <el-link
                  style="margin-left:10px"
                  type="text"
                  size="medium"
                  :underline="false"
                  @click="addCodeReview(scope.row.fslipno, scope.row.fobjectid)"
                  >代码Review</el-link
                >
                <el-link
                  style="margin-left:10px"
                  type="text"
                  size="medium"
                  :underline="false"
                  @click="openQaTestList(scope.row.id, scope.row.fobjectid)"
                  >测试</el-link
                >
                <el-link
                  style="margin-left:10px"
                  type="primary"
                  :underline="false"
                  v-show="scope.row.qadfcount === 0"
                  @click="deleteQaHead(scope.row.id, scope.row.fobjectid)"
                  icon="el-icon-delete"
                ></el-link>
              </template>
            </el-table-column>
          </el-table></div
      ></el-col>
      <el-col :xs="2" :sm="3" :md="3" :lg="4" :xl="4"><div></div></el-col>
    </el-row>
    <QaObjectSummary ref="QaObjectSummary"></QaObjectSummary>

    <QaDesignReview ref="QaDesignReview" :isdisable="isdisable"></QaDesignReview>
    <QaCodeReview ref="QaCodeReview" :isdisable="isdisable"></QaCodeReview>
  </div>
</template>

<script>
import { getSingleLiaisonBySlipNo } from "./../../../services/liaisonService";
import {
  getQaHeadBySlipNo,
  newQaHead,
  deleteQaHead,
} from "./../../../services/qaService";
import QaObjectSummary from "./QaObjectSummary";
import QaDesignReview from "./QaDesignReview";
import QaCodeReview from "./QaCodeReview";
export default {
  components: {
    QaObjectSummary,
    QaDesignReview,
    QaCodeReview,
  },
  data() {
    return {
      isdisable:false,
      loading:false,
      liaison: {},
      qaheads: [],
      form: {
        fsystemcd: "",
        fprojectcd: "",
        fslipno: "",
        fobjectid: "",
        fstatus: "1",
        ftesttyp: "MCL",
      },
      rules: {
        fobjectid: [
          { required: true, message: "请输入测试对象名称", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    onSubmit(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          var resp = await newQaHead(this.form);
          if (resp.status === 201) {
            this.refreshQaHead(this.liaison.fslipno);
            this.$message({
              message: "测试对象" + this.form.fobjectid + "创建成功！",
              type: "success",
            });
            this.$refs[formName].resetFields();
          }
        }
      });
    },

    addObjectSummary(id) {
      this.$refs.QaObjectSummary.handleDialog(id);
    },

    addDesignReview(slipno) {
      this.$refs.QaDesignReview.handleDialog(slipno);
    },

    addCodeReview(slipno, objectid) {
      this.$refs.QaCodeReview.handleDialog(slipno, objectid);
    },

    openQaTestList(id, obj) {
      this.$router.push({
        name: "QaTestList",
        query: { qahf_id: id, object: obj },
      });
    },

    deleteQaHead(id, fobjectid) {
      this.$confirm("此操作将永久删除" + fobjectid + ", 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async (action) => {
          if (action === "confirm") {
            var resp = await deleteQaHead(id);
            if (resp.status == 204) {
              this.refreshQaHead(this.liaison.fslipno);
              this.$message({
                message: fobjectid + "已经删除！",
                type: "success",
              });
            } else {
              this.$message.error(fobjectid + "删除失败");
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

    async refreshQaHead(slipno) {
      var qa_resp = await getQaHeadBySlipNo(slipno);
      this.qaheads = [];
      if (qa_resp.status === 200) {
        var qaH = qa_resp.data;
        for (var i in qaH) {
          var fstatus = qaH[i].fstatus;
          if (fstatus === "1") {
            qaH[i].fstatus = "初始";
            qaH[i].tagtype = "info";
          } else if (fstatus === "2") {
            qaH[i].fstatus = "已审核";
            qaH[i].tagtype = "";
          } else if (fstatus === "3") {
            qaH[i].fstatus = "已提交";
            qaH[i].tagtype = "warning";
          } else {
            qaH[i].fstatus = "已确认";
            qaH[i].tagtype = "success";
          }
        }
        this.qaheads = qaH;
      }
    },
  },
  mounted: async function() {
    this.loading = true;
    var slipno = this.$route.query.slipno;
    var resp = await getSingleLiaisonBySlipNo(slipno).catch(() => {
      this.$message.error("联络票号:" + slipno + "数据获取异常");
    });

    if (resp.status === 200) {
      this.liaison = resp.data.results[0];
      this.form.fslipno = this.liaison.fslipno;
      this.form.fsystemcd = this.liaison.fsystemcd;
      this.form.fprojectcd = this.liaison.fprojectcd;
      if(this.liaison.fstatus === '4'){
        this.isdisable = true
      }else{
        this.isdisable = false
      }
    }
    this.refreshQaHead(slipno);
    this.loading = false
  },
};
</script>

<style scoped>
.table-height {
  height: calc(100vh - 100);
}
.el-table--medium td,
.el-table--medium th {
  padding: 5px 0px;
}
.el-table__row {
  height: 20px;
}
.el-table__header {
  padding: 0;
}
.body-style {
  padding: 8px 10px;
}
</style>
