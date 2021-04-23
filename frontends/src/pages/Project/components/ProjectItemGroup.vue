<template>
  <div style="margin-left:60px">
    <el-row :gutter="12">
      <el-col
        v-for="(item, index) in orderInfo"
        :key="item.orderno"
        :span="11"
        class="card-style"
      >
        <el-card shadow="hover" class="card-shadow" :class="gapClass(index)">
          <div slot="header" class="clearfix">
            <el-row>
              <el-col :span="23"
                ><div>
                  <h6 class="clear-margin-padding hidden-text">
                    {{ item.organization }} - {{ item.project }} - [{{
                      item.orderno
                    }}
                    ]
                  </h6>
                </div></el-col
              >
              <el-col :span="1">
                <p :class="statusClass(item)"></p>
              </el-col>
            </el-row>
          </div>
          <div
            @click="openProjectOverView(item.orderno)"
            class="mouse_style_link"
          >
            <el-row>
              <el-col :span="23"
                ><div>
                  <h6 class="clear-margin-padding hidden-text">
                    {{ item.note }}
                  </h6>
                </div></el-col
              >
              <el-col :span="1">
                <el-dropdown @command="handleOrder">
                  <span class="el-dropdown-link">
                    <i class="el-icon-more"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item
                      :command="beforeHandleOrder('report', item.orderno)"
                      >报表</el-dropdown-item
                    >
                    <el-dropdown-item :disabled="true">分析</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24"><div style="height:40px"></div></el-col>
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
                  {{ item.partner }}
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
                  {{ item.slipno_all }}
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
                  {{ item.slipno_close }}
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
                  {{ item.slipno_working }}
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
                  {{ item.objectcount }}
                </div></el-col
              >
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <div>
      <el-pagination
        background
        layout="prev, pager, next"
        :hide-on-single-page="true"
        :total="orderTotal"
        :page-size="pageSize"
        :current-page="currentPage"
        :page-count="pageCount"
        @current-change="handlePage"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getQaProjectGroup } from "../../../services/projectService";
export default {
  data: function() {
    return {
      currentPage: 1,
      orderTotal: 0,
      pageSize: 6,
      pageCount: 1,
      currentID: 0,
      orderInfo: [],
      query_organization_id: "",
      query_project_code: "",
      query_order_no: "",
    };
  },
  methods: {
    handleOrder(command) {
      console.log(command);
      var type = command.type;
      var order_no = command.order_no;
      if (type === "report") {
        this.$router.push({ name: "Report", query: { order_no: order_no } });
      }
    },

    beforeHandleOrder(type, order_no) {
      return {
        type: type,
        order_no: order_no,
      };
    },

    gapClass(index) {
      if (index === 4 || index === 5) {
        return "gap-style-bottom";
      } else {
        return "gap-style";
      }
    },

    statusClass(item) {
      if (item.status === 4) {
        return "is-end";
      } else {
        return "is-working";
      }
    },

    openProjectOverView(order) {
      this.$router.push({
        name: "ProjectOverview",
        query: { order_no: order },
      });
    },

    handlePage(page) {
      this.currentPage = page;
      this.getProjectItems(
        this.query_organization_id,
        this.query_project_code,
        this.query_order_no
      );
    },

    calcPageTotal(liaisonCount, pageSize) {
      liaisonCount = this.liaisonTotal;
      pageSize = this.pageSize;
      var remainder = liaisonCount % pageSize;
      if (remainder === 0) {
        this.pageCount = liaisonCount / pageSize;
      } else {
        this.pageCount = parseInt(liaisonCount / pageSize) + 1;
      }
    },

    // refreshProjectItems() {
    //   this.getProjectItems();
    // },
    //按升序排列
    up(x, y) {
      return x.status - y.status;
    },
    async getProjectItems(
      query_organization_id,
      query_project_code,
      query_order_no
    ) {
      this.query_organization_id = query_organization_id;
      this.query_project_code = query_project_code;
      this.query_order_no = query_order_no;
      var resp = await getQaProjectGroup(
        query_organization_id,
        query_project_code,
        query_order_no,
        this.currentPage,
        this.pageSize
      );
      if (resp.status === 200) {
        this.orderTotal = resp.data.count;
        this.calcPageTotal(this.orderTotal, this.pageSize);
        this.orderInfo = resp.data.results;
        this.orderInfo.sort(this.up);
      } else {
        this.$message.error("项目明细获取失败");
      }
    },
  },
  mounted: function() {
    this.getProjectItems(
      this.query_organization_id,
      this.query_project_code,
      this.query_order_no
    );
  },
};
</script>

<style>
/* .card-color-1 {
  background-color: #f4f3f3;
}

.card-color-2 {
  background-color: #f87d42;
}

.card-color-3 {
  background-color: #db3951;
}

.card-color-4 {
  background-color: #00136c;
} */

.gap-style-bottom {
  margin-right: 40px;
}

.gap-style {
  margin-right: 40px;
  margin-bottom: 40px;
}

.is-working {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #03c4a1;
}

.is-end {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #00303f;
}

.hidden-text {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}

.card-shadow {
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
}

.el-card__header {
  padding: 0;
  border-bottom: 1px solid #ebeef5;
  box-sizing: border-box;
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
/* .clear-margin-padding {
  margin: 0px;
  padding: 0px;
} */
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
.mouse_style_link {
  cursor: pointer;
}
</style>
