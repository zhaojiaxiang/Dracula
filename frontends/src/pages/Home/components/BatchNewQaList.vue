<template>
  <el-dialog title="批量添加测试用例" :visible.sync="dialogFormVisible">
    <el-form>
      <el-form-item>
        <el-input
          disabled
          autofocus="true"
          placeholder="Ctrl+V实现测试Case粘贴并自动批量添加"
        ></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button
        id="submitbtn"
        type="primary"
        @click="onBatchSubmit"
        v-loading.fullscreen.lock="fullscreenLoading"
        >确 定</el-button
      >
      <el-button @click="dialogFormVisible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { newQaDetail } from "./../../../services/qaService";
export default {
  data() {
    return {
      dialogFormVisible: false,
      qaheadid: 0,
      qadetails: [],
      fullscreenLoading: false,
    };
  },
  mounted() {
    this.$el.addEventListener("paste", (event) => {
      event.stopPropagation();
      event.preventDefault(); //消除默认粘贴

      this.qadetails = [];

      var clipboardData = event.clipboardData || window.clipboardData;
      var pastedData = clipboardData.getData("Text");

      this.qadetails = pastedData
        .split("\n")
        .filter(function(item) {
          //兼容Excel行末\n，防止出现多余空行
          return item !== "";
        })
        .map(function(item) {
          return item.split("\t");
        });

      document.getElementById("submitbtn").click();
    });
  },
  methods: {
    handleDialog(id) {
      this.dialogFormVisible = !this.dialogFormVisible;
      this.qaheadid = id;
    },

    async onBatchSubmit() {
      this.fullscreenLoading = true;

      // if (this.qadetails.length === 0) {
      //   this.$message.error("粘贴板中数据为空或者异常");
      //   this.fullscreenLoading = false;
      //   this.qadetails = [];
      //   return;
      // }

      for (var i in this.qadetails) {
        if (this.qadetails[i].length < 2) {
          this.$message.error(
            "粘贴文本格式错误: 测试用例，分类(非必须)，排序规则(非必须)"
          );
          this.fullscreenLoading = false;
          this.qadetails = [];
          return;
        }
        if (this.qadetails[i].length === 2) {
          this.qadetails[i][2] = "";
          this.qadetails[i][3] = "";
        }
        if (this.qadetails[i].length === 3) {
          this.qadetails[i][3] = "";
        }
        if (!(this.qadetails[i][0] === "Y" || this.qadetails[i][0] === "N")) {
          var rownum = parseInt(i) + 1;
          this.$message.error("第" + rownum + "行，回归测试只能为 Y 或者 N");
          this.fullscreenLoading = false;
          this.qadetails = [];
          return;
        }

        var form = {};
        form["fregression"] = this.qadetails[i][0];
        form["fcontent"] = this.qadetails[i][1];
        form["fclass1"] = this.qadetails[i][2];
        form["fclass2"] = "";
        form["fsortrule"] = this.qadetails[i][3];
        form["qahf"] = this.qaheadid;

        var resp = await newQaDetail(form).catch(() => {
          this.$message.error("批量添加测试项异常");
          this.$emit("refreshQaList");
          this.dialogFormVisible = false;
          this.fullscreenLoading = false;
          this.qadetails = [];
          return;
        });

        if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
          this.$message.error(resp.data.message);
          this.$emit("refreshQaList");
          this.dialogFormVisible = false;
          this.fullscreenLoading = false;
          this.qadetails = [];
          return;
        }
      }
      this.$emit("refreshQaList");
      this.dialogFormVisible = false;
      this.fullscreenLoading = false;
      this.qadetails = [];
    },
  },
};
</script>

<style scoped>
.width-sytle {
  width: 90%;
}
</style>
