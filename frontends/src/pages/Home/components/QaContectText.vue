<template>
  <div>
    <div style="margin:10px">
      <el-page-header @back="goBack" :content="qadf.fcontent"> </el-page-header>
    </div>

    <Myeditor
      @handleContentText="submitContentText"
      v-show="isshow"
      :editorData="content_text"
      :isdisable="isdisable"
      @receivedata="receivedata"
    ></Myeditor>
    <MyReadOnlyeditor :proofs="proofs"></MyReadOnlyeditor>
  </div>
</template>

<script>
import Myeditor from "../../Commond/Myeditor";
import MyReadOnlyeditor from "../../Commond/MyReadOnlyeditor";
import {
  getQaDetailContentText,
  updateQaDetailContentText,
  getQadetailProofContentText,
  approvalQaDetailContentText,
} from "../../../services/qaService";
export default {
  components: {
    Myeditor,
    MyReadOnlyeditor,
  },
  data() {
    return {
      operate_type: "",
      isshow: true,
      isdisable: false,
      content_text: "",
      qadf: {},
      proofs: [],
    };
  },
  methods: {
    receivedata(e) {
      this.content_text = e;
    },
    goBack() {
      window.history.go(-1);
    },
    async submitContentText(val) {
      this.qadf.fcontent_text = val;
      var resp;
      if (this.operate_type === "test") {
        resp = await updateQaDetailContentText(this.qadf.id, this.qadf).catch(
          () => {
            this.$message.error("测试贴图提交异常");
          }
        );
      } else if (this.operate_type === "approval") {
        resp = await approvalQaDetailContentText(this.qadf.id, this.qadf).catch(
          () => {
            this.$message.error("测试贴图提交异常");
          }
        );
      }
      if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.success("测试贴图提交成功");
        this.bus.$emit("refreshList");
        window.history.go(-1);
      }
    },

    async getQadetailProofContentText(id) {
      var resp = await getQadetailProofContentText(id).catch(() => {
        this.$message.error("测试评论数据获取异常");
      });
      if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.proofs = resp.data;
      } else {
        this.$message.error(resp.data.message);
      }
    },
  },
  mounted: async function() {
    var id = this.$route.query.qadf_id;
    //operate_type为操作类型，是测试、还是审核
    this.operate_type = this.$route.query.type;
    var resp = await getQaDetailContentText(id).catch(() => {
      this.$message.error("测试贴图信息获取异常");
    });
    this.qadf = resp.data;

    if (resp.data.status === "4") {
      this.isshow = false;
    }

    if (resp.data.status === "3" || resp.data.status === "4") {
      this.isdisable = true;
    } else {
      this.isdisable = false;
    }

    this.content_text = this.qadf.fcontent_text;

    await this.getQadetailProofContentText(id);

    if (this.proofs.length > 0) {
      // first_content_type 是测试贴图列表中第一条数据的类型
      var first_content_type = this.proofs[0].type;

      if (this.operate_type === "test") {
        this.isshow = true;
        if (first_content_type === "A") {
          this.content_text = "";
        } else if (first_content_type === "T") {
          this.content_text = this.proofs[0].fcontent_text;
          this.proofs = this.proofs.slice(1);
        }
      } else if (this.operate_type === "approval") {
        this.isdisable = false;
        if (first_content_type === "A") {
          this.content_text = this.proofs[0].fcontent_text;
          this.proofs = this.proofs.slice(1);
        } else if (first_content_type === "T") {
          this.content_text = "";
        }
      }
    }else{
      if (this.operate_type === "approval"){
        this.isdisable = false;
      }
    }
  },
};
</script>

<style></style>
