<template>
  <div class="goTop">
    <el-row>
      <el-col :span="15"
        ><div>
          <el-breadcrumb
            separator-class="el-icon-arrow-right"
            style="font-size:16px;margin-top: 5px;"
          >
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item
              v-show="paramtype !== 'pcl'"
              :to="{ path: '/qa/', query: { slipno: this.qahead.fslipno } }"
              >QA列表</el-breadcrumb-item
            >
            <el-breadcrumb-item
              v-show="paramtype === 'pcl'"
              :to="{ path: '/task/', query: { type: this.paramtype } }"
              >任务列表</el-breadcrumb-item
            >
            <el-breadcrumb-item
              v-show="paramtype === 'pcl'"
              :to="{
                name: 'QaPclClass1',
                query: {
                  qahf_id: this.qahead.id,
                  type: this.paramtype,
                  class1: class1,
                },
              }"
              >PCL列表 -- {{ this.qahead.fobjectid }}</el-breadcrumb-item
            >
            <el-breadcrumb-item>{{ this.class1 }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div></el-col
      >
      <el-col :span="9">
        <div>
          <PCLTargetActual></PCLTargetActual>
        </div>
      </el-col>
    </el-row>

    <el-row style="margin-top:5px"> </el-row>
    <el-table
      ref="multipleTable"
      :data="qadetails"
      tooltip-effect="dark"
      border
      size="medium"
      style="width: 98%; margin-top:5px"
      v-loading="loading"
      class="card-shadow"
    >
      <el-table-column label="序号" type="index" width="50"> </el-table-column>
      <el-table-column
        prop="fclass2"
        label="分类2"
        width="400"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <el-link
            @click="openDetail(scope.row.fclass2)"
            type="primary"
            :underline="false"
            >{{ scope.row.fclass2 }}</el-link
          >
        </template>
      </el-table-column>
      <el-table-column prop="test_cnt" label="测试用例数量" width="150">
      </el-table-column>
      <el-table-column prop="tested_cnt" label="已经测试数量" width="150">
      </el-table-column>
      <el-table-column prop="ng" label="未处理NG数量" width="150">
      </el-table-column>
      <el-table-column prop="canceled_cnt" label="取消数量" width="150">
      </el-table-column>
    </el-table>

    <el-backtop target=".goTop" :bottom="100">
      <i class="el-icon-caret-top"></i>
    </el-backtop>
  </div>
</template>

<script>
import { getQaHead, getPclQaClass2 } from "./../../../services/qaService";
import PCLTargetActual from "../components/PCLTargetActual";
export default {
  components: {
    PCLTargetActual,
  },
  data() {
    return {
      loading: false,
      paramtype: "",
      fullscreenLoading: false,
      class1: "",
      qahead: {},
      qadetails: [],
      multipleSelection: [],
    };
  },

  methods: {
    filterResult(value, row) {
      return row.fresult === value;
    },
    openDetail(class2) {
      this.$router.push({
        name: "QaPclList",
        query: {
          qahf_id: this.qahead.id,
          type: this.paramtype,
          class1: this.class1,
          class2: class2,
        },
      });
    },
  },
  mounted: async function() {
    this.loading = true;
    var id = this.$route.query.qahf_id;
    this.class1 = this.$route.query.class1;
    this.paramtype = this.$route.query.type;
    var resp = await getQaHead(id).catch(() => {
      this.$message.error("测试对象数据获取异常");
    });

    if (resp.status === 200) {
      this.qahead = resp.data;
    }

    var resp_class2 = await getPclQaClass2(this.qahead.id, this.class1).catch(
      () => {
        this.$message.error("分类2数据获取异常");
      }
    );

    if (resp_class2.status === 200) {
      this.qadetails = resp_class2.data[0].class2;
    }

    this.loading = false;
  },
};
</script>

<style>
.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}
.goTop {
  height: calc(100vh - 70px);
  overflow-x: hidden;
}
.el-table--medium td,
.el-table--medium th {
  padding: 2px 0px;
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
.div-style {
  margin: 0px;
}
</style>
