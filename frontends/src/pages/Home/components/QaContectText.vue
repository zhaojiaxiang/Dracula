<template>
  <div>
      <div style="margin:10px">
          <el-page-header @back="goBack" :content="qadf.fcontent"> </el-page-header>
      </div>
    
    <Myeditor
      @handleContentText="submitContentText"
      :editorData="qadf.fcontent_text"
      :isdisable="isdisable"
    ></Myeditor>
  </div>
</template>

<script>
import Myeditor from "../../Commond/Myeditor";
import {
  getQaDetailContentText,
  updateQaDetailContentText,
} from "../../../services/qaService";
export default {
  components: {
    Myeditor,
  },
  data() {
    return {
      isdisable:false,
      qadf: {},
    };
  },
  methods: {
    goBack() {
      window.history.go(-1);
    },
    async submitContentText(val) {
      this.qadf.fcontent_text = val;
      var resp = await updateQaDetailContentText(this.qadf.id, this.qadf).catch(
        () => {
          this.$message.error("测试贴图提交异常");
        }
      );
      if (!Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.success("测试贴图提交成功");
        this.bus.$emit("refreshList");
        window.history.go(-1);
      }
    },
  },
  mounted: async function() {
    var id = this.$route.query.qadf_id;
    var resp = await getQaDetailContentText(id).catch(() => {
      this.$message.error("测试贴图信息获取异常");
    });
    this.qadf = resp.data;
    if(resp.data.status === '3'|| resp.data.status === '4'){
      this.isdisable = true
    }else{
      this.isdisable = false
    }
  },
};
</script>

<style></style>
