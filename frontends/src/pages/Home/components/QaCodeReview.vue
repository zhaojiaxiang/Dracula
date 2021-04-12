<template>
  <div>
    <el-dialog title="填写代码Review" :visible.sync="dialogFormVisible">
      <el-form ref="form">
        <el-form-item>
          <Myeditor
            @handleContentText="updateQaCodeReview"
            :editorData="contentText"
            :isdisable="isdisable"
            @receivedata="receivedata"
          ></Myeditor>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getCodeReview,
  newCodeReview,
  updateCodeReview,
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
      objectid: "",
      query_objectid: "",
      id: 0,
    };
  },
  methods: {
    receivedata(e){
      this.content_text=e;
    },

    async handleDialog(slipno, objectid) {
      this.slipno = slipno;
      this.objectid = objectid;
      this.query_objectid = objectid.replace(/ /g, "+");
      this.dialogFormVisible = !this.dialogFormVisible;
      var resp = await getCodeReview(slipno, this.query_objectid).catch(() => {
        this.$message.error("代码Review数据获取异常");
        return;
      });
      if (resp.data.length !== 0) {
        this.contentText = resp.data[0].fcontent_text;
        this.id = resp.data[0].id;
      }
    },
    async updateQaCodeReview(val) {
      var form = {
        fslipno: this.slipno,
        fobjectid: this.objectid,
        fcontent_text: val,
      };

      var resp = await getCodeReview(this.slipno, this.query_objectid).catch(
        () => {
          this.$message.error("代码Review数据获取异常");
          return;
        }
      );

      var resp_up;
      if (resp.data.length !== 0) {
        resp_up = await updateCodeReview(resp.data[0].id, form).catch(() => {
          this.$message.error("代码Review数据更新异常");
          return;
        });
      } else {
        resp_up = await newCodeReview(form).catch(() => {
          this.$message.error("代码Review数据新建异常");
          return;
        });
      }
      if (Object.prototype.hasOwnProperty.call(resp_up.data, "message")) {
        this.$message.error(resp_up.data.message);
      } else {
        this.$message.success("操作成功");
        this.dialogFormVisible = false;
      }
    },
  },
};
</script>

<style></style>
 