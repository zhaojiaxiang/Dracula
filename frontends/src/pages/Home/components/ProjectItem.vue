<template>
  <div>
    <el-row :gutter="12">
      <el-col
        v-for="item in orderInfo"
        :key="item.order_no"
        :span="7"
        class="card-style"
      >
        <el-card shadow="hover" class="card-color card-shadow mouse_style_link">
          <div @click="openProjectOverView(item.order_no)">
            <el-row>
              <el-col :span="24"
                ><div>
                  <h6 class="clear-margin-padding">
                   {{ item.project }} - [ {{ item.order_no }} ]
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div>
                  <h6 class="clear-margin-padding">
                    {{ item.order_note }}
                  </h6>
                </div></el-col
              >
            </el-row>
            <el-row>
              <el-col :span="24"
                ><div>
                  <el-steps :active="item.order_status" finish-status="success">
                    <el-step title="未开始" class="step-style"></el-step>
                    <el-step title="已开始"></el-step>
                    <el-step title="已结束"></el-step>
                    <el-step title="已发布"></el-step>
                  </el-steps></div
              ></el-col>
            </el-row>
            <el-row class="icon-style">
              <el-col :span="4"
                ><div>
                  <el-tooltip
                    class="item"
                    effect="dark"
                    content="参与人"
                    placement="bottom"
                    ><i class="el-icon-user"></i
                  ></el-tooltip>
                  {{ item.order_partner }}
                </div></el-col
              >
              <el-col :span="4"
                ><div>
                  <el-tooltip
                    class="item"
                    effect="dark"
                    content="联络票"
                    placement="bottom"
                    ><i class="el-icon-tickets"></i
                  ></el-tooltip>
                  {{ item.order_slipno_all }}
                </div></el-col
              >
              <el-col :span="4">
                <div>
                  <el-tooltip
                    class="item"
                    effect="dark"
                    content="已完成"
                    placement="bottom"
                    ><i class="el-icon-finished"></i
                  ></el-tooltip>
                  {{ item.order_slipno_close }}
                </div></el-col
              >
              <el-col :span="4"
                ><div>
                  <el-tooltip
                    class="item"
                    effect="dark"
                    content="未完成"
                    placement="bottom"
                    ><i class="el-icon-s-flag"></i
                  ></el-tooltip>
                  {{ item.order_slipno_working }}
                </div></el-col
              >
              <el-col :span="4"
                ><div>
                  <el-tooltip
                    class="item"
                    effect="dark"
                    content="测试对象"
                    placement="bottom"
                    ><i class="el-icon-lollipop"></i
                  ></el-tooltip>
                  {{ item.test_object }}
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
import { myOrderInfo } from "../../../services/liaisonService";
export default {
  data: function() {
    return {
      orderInfo: [],
    };
  },
  methods: {

    openProjectOverView(order){
      this.$router.push({name:'ProjectOverview',query: {order_no: order}})
    },
    refreshProjectItems() {
      this.getProjectItems();
    },
    async getProjectItems() {
      var resp = await myOrderInfo();
      if (resp.status === 200) {
        this.orderInfo = resp.data;
      } else {
        this.$message.error("我的参与项目明细获取失败");
      }
    },
  },
  mounted: function() {
    this.getProjectItems();
  },
};
</script>

<style>
.card-color {
  background-color:'';
}

.card-shadow {
  box-shadow:4px 4px 40px rgba(0,0,0,.05)
}

.card-style {
  padding-bottom: 0px;
  margin-bottom: 10px;
}
.el-card__body {
  padding: 0;
}
.icon-style {
  color: #8c92a4;
  font-size: 14px;
}
.clear-margin-padding {
  margin: 0px;
  padding: 0px;
}
.el-step__title {
  font-size: 10px;
  line-height: 20px;
}
.step-style {
  size: 4px;
}
.el-row {
  margin: 10px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.mouse_style_link{
  cursor:pointer;  
}
</style>
