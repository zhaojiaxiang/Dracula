<template>
  <div>
    <el-row>
      <el-col>
        <div style="margin-right:40px; margin-left:20px; margin-top:200px">
          <ckeditor
            style="border:1px solid hsla(0, 0%, 0%, 0.15)"
            id="editor"
            :editor="editor"
            v-model="editorData"
            :config="editorConfig"
          ></ckeditor>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import BalloonBlockEditor from "@ckeditor/ckeditor5-build-balloon-block";
export default {
  data() {
    return {
      editor: BalloonBlockEditor,

      editorConfig: {
        title:"this is title",
        placeholder: "请填写内容",
        blockToolbar: {
          items: [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "undo",
            "redo",
            "numberedList",
            "bulletedList",
            "todoList",
            "outdent",
            "indent",
            "removeFormat",
            "|",
            "imageInsert",
            // "imageResize",
            // "imageTextAlternative",
            "|",
            "highlight",
            "code",
            "codeBlock",
            "insertTable",
          ],
          shouldNotGroupWhenFull: false
        },
      },
    };
  },
};
</script>

<style>
/*编辑框最低高度*/
.ck-editor__editable {
  min-height: 200px;
}
</style>
