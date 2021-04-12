<template>
  <div>
    <el-dialog title="填写设计Review" :visible.sync="dialogFormVisible">
      <el-form ref="form">
        <el-form-item>
          <Myeditor
            @handleContentText="updateQaDesignReview"
            :editorData="contentText"
            :isdisable="isdisable"
          ></Myeditor>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDesignReview,
  newDesignReview,
  updateDesignReview,
} from "./../../../services/qaService";
import Myeditor from "../../Commond/Myeditor";
export default {
  components: {
    Myeditor,
  },
  props:['isdisable'],
  data() {
    return {
      dialogFormVisible: false,
      contentText: "",
      slipno: "",
      id: 0,
    };
  },
  methods: {
    async handleDialog(slipno) {
      var objectid = "Design+Review"
      this.slipno = slipno;
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getDesignReview(slipno, objectid).catch(() => {
        this.$message.error("设计Review数据获取异常");
        return;
      });
      if (resp.data.length !== 0) {
        this.contentText = resp.data[0].fcontent_text;
        this.id = resp.data[0].id;
      }
    },
    async updateQaDesignReview(val) {
      var objectid = "Design+Review"
      var form = {
        fslipno: this.slipno,
        fobjectid: "Design Review",
        fcontent_text: val,
      };

      var resp = await getDesignReview(this.slipno, objectid).catch(
        () => {
          this.$message.error("设计Review数据获取异常");
          return;
        }
      );

      var resp_up;
      if (resp.data.length !== 0) {
        resp_up = await updateDesignReview(resp.data[0].id, form).catch(() => {
          this.$message.error("设计Review数据更新异常");
          return;
        });
      } else {
        resp_up = await newDesignReview(form).catch(() => {
          this.$message.error("设计Review数据新建异常");
          return;
        });
      }
      if(Object.prototype.hasOwnProperty.call(resp_up.data, 'message')){
        this.$message.error(resp_up.data.message);
      }else{
        this.$message.success("操作成功");
        this.dialogFormVisible = false
      }
    },
  },
};
</script>

<style></style>
