<template>
  <div>
    <el-dialog title="填写设计Review" :visible.sync="dialogFormVisible">
    <el-form ref="form" :rules="rules" :model="form">
      <el-form-item prop="fcontent" required>
        <Myeditor></Myeditor>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="onSubmit('form')">确 定</el-button>
      <el-button @click="resetForm('form')">重 置</el-button>
      <el-button @click="dialogFormVisible = false">取 消</el-button>
    </div>
  </el-dialog>
  </div>
</template>

<script>
import Myeditor from "../../Commond/Myeditor";
export default {
  components:{
    Myeditor
  }
}
</script>

<style>

</style>