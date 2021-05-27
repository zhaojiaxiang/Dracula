<template>
  <div>
    <div style="margin:10px">
      <el-page-header @back="goBack"></el-page-header>
    </div>
    <el-row :gutter="10">
      <el-col :xs="2" :sm="3" :md="3" :lg="4" :xl="4"><div></div></el-col>
      <el-col :xs="20" :sm="18" :md="18" :lg="16" :xl="16"
        ><div>
          <el-form
            :model="liaison"
            style=" margin-top:20px;"
          >
            <el-form-item>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="liaison.fsystemcd" disabled></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item>
                  <el-input v-model="liaison.fprojectcd" disabled></el-input>
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
                  <el-input v-model="liaison.fslipno" disabled></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8">
              </el-col>
              <el-col :span="8">
                <el-form-item>
                  <el-button type="text" @click="addDesignReview(liaison.fslipno)"
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
            class="card-shadow"
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
import { getSingleALlLiaisonBySlipNo } from "../../../services/liaisonService";
import {
  getQaHeadBySlipNo,
} from "../../../services/qaService";
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
    };
  },
  methods: {
    goBack() {
      //返回上一个路由
      this.$router.go(-1)
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
    var resp = await getSingleALlLiaisonBySlipNo(slipno).catch(() => {
      this.$message.error("联络票号:" + slipno + "数据获取异常");
    });
    console.log(resp);
    if (resp.status === 200) {
      this.liaison = resp.data.results[0];
    }
    this.refreshQaHead(slipno);
    this.loading = false
  },
};
</script>

<style scoped>
.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
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
