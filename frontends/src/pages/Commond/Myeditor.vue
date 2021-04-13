<template>
  <div>
    <el-row>
      <el-col>
        <div style="margin-right:40px; margin-left:20px">
          <ckeditor
            id="editor"
            @ready="onReady"
            :editor="editor"
            :value="editorData"
            :config="editorConfig"
            @input="receivedata"
          ></ckeditor>
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="12">
        <div style="margin-left:20px;margin-top:10px">


          <el-upload
            class="upload-demo"
            :before-upload="beforeFileUpload"
            action="/api/file_upload/">
            <el-button slot="trigger" v-show="!isdisable" type="primary">上传文件</el-button>
            <!-- <div slot="tip" class="el-upload__tip">文件大小不可超过 2MB</div> -->
          </el-upload>
        </div>
      </el-col>
      <el-col :span="12">
        <div style="text-align:right;margin-right:40px; margin-top:10px">
          <el-button type="primary" v-show="!isdisable" @click="handle()">提交</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CKEditor from "@ckeditor/ckeditor5-vue2";
import ClassicEditor from "@ckeditor/ckeditor5-editor-classic/src/classiceditor";

import EssentialsPlugin from "@ckeditor/ckeditor5-essentials/src/essentials";
import BoldPlugin from "@ckeditor/ckeditor5-basic-styles/src/bold";
import ItalicPlugin from "@ckeditor/ckeditor5-basic-styles/src/italic";
import CodePlugin from "@ckeditor/ckeditor5-basic-styles/src/code";
import LinkPlugin from "@ckeditor/ckeditor5-link/src/link";
import ParagraphPlugin from "@ckeditor/ckeditor5-paragraph/src/paragraph";
import Heading from "@ckeditor/ckeditor5-heading/src/heading";

import Image from "@ckeditor/ckeditor5-image/src/image";
import ImageInsert from "@ckeditor/ckeditor5-image/src/imageinsert";
import ImageToolbar from "@ckeditor/ckeditor5-image/src/imagetoolbar";
// import ImageCaption from "@ckeditor/ckeditor5-image/src/imagecaption";
import ImageStyle from "@ckeditor/ckeditor5-image/src/imagestyle";
import ImageResize from "@ckeditor/ckeditor5-image/src/imageresize";
import ImageResizeEditing from "@ckeditor/ckeditor5-image/src/imageresize/imageresizeediting";
import ImageResizeHandles from "@ckeditor/ckeditor5-image/src/imageresize/imageresizehandles";

import Highlight from "@ckeditor/ckeditor5-highlight/src/highlight";
import RemoveFormat from "@ckeditor/ckeditor5-remove-format/src/removeformat";
import PasteFromOffice from "@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice";
import CodeBlock from "@ckeditor/ckeditor5-code-block/src/codeblock";
import ListStyle from "@ckeditor/ckeditor5-list/src/liststyle";
import TodoList from "@ckeditor/ckeditor5-list/src/todolist";
import TextTransformation from "@ckeditor/ckeditor5-typing/src/texttransformation";
import Table from "@ckeditor/ckeditor5-table/src/table";
import TableToolbar from "@ckeditor/ckeditor5-table/src/tabletoolbar";
import BlockToolbar from "@ckeditor/ckeditor5-ui/src/toolbar/block/blocktoolbar";
import Indent from "@ckeditor/ckeditor5-indent/src/indent";
import IndentBlock from "@ckeditor/ckeditor5-indent/src/indentblock";

import MyUploadAdapter from "../../services/ckeditorService";
import { fileUpdate } from "../../services/qaService";

export default {
  components: {
    // Use the <ckeditor> component in this view.
    ckeditor: CKEditor.component,
  },
  props: ['editorData', 'isdisable'],
  data() {
    return {
      outEditorData:"",
      editor: ClassicEditor,
    //   editorData: this.contentText,
      editorConfig: {
        placeholder: "请填写内容",
        plugins: [
          BlockToolbar,
          EssentialsPlugin,
          CodePlugin,
          BoldPlugin,
          ItalicPlugin,
          LinkPlugin,
          ParagraphPlugin,
          Heading,
          Image,
          ImageInsert,
          ImageToolbar,
          ImageStyle,
          ImageResize,
          ImageResizeEditing,
          ImageResizeHandles,
          Highlight,
          RemoveFormat,
          RemoveFormatLinks,
          PasteFromOffice,
          CodeBlock,
          ListStyle,
          TodoList,
          TextTransformation,
          Table,
          TableToolbar,
          Indent,
          IndentBlock,
        ],

        toolbar: {
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
        },

        table: {
          contentToolbar: ["tableColumn", "tableRow", "mergeTableCells"],
        },

        image: {
            // Configure the available styles.
            styles: [
                'alignLeft', 'alignCenter', 'alignRight'
            ],

            // Configure the available image resize options.
            resizeOptions: [
                {
                    name: 'imageResize:original',
                    label: 'Original',
                    value: null
                },
                {
                    name: 'imageResize:50',
                    label: '50%',
                    value: '50'
                },
                {
                    name: 'imageResize:75',
                    label: '75%',
                    value: '75'
                }
            ],

            // You need to configure the image toolbar, too, so it shows the new style
            // buttons as well as the resize buttons.
            toolbar: [
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight',
                '|',
                'imageResize',
                '|',
                'imageTextAlternative'
            ]
        },

        heading: {
          options: [
            {
              model: "paragraph",
              title: "Paragraph",
              class: "ck-heading_paragraph",
            },
            {
              model: "heading1",
              view: "h1",
              title: "Heading 1",
              class: "ck-heading_heading1",
            },
            {
              model: "heading2",
              view: "h2",
              title: "Heading 2",
              class: "ck-heading_heading2",
            },
            {
              model: "heading3",
              view: "h3",
              title: "Heading 3",
              class: "ck-heading_heading3",
            },
            {
              model: "heading4",
              view: "h4",
              title: "Heading 4",
              class: "ck-heading_heading4",
            },
            {
              model: "heading5",
              view: "h5",
              title: "Heading 5",
              class: "ck-heading_heading5",
            },
            {
              model: "heading6",
              view: "h6",
              title: "Heading 6",
              class: "ck-heading_heading6",
            },
          ],
        },
      },
    };
  },
  methods: {
    handle() {
      this.$emit("handleContentText", this.outEditorData);
    },
    receivedata(e){
      this.$emit("receivedata", e);
      this.outEditorData=e;
    },
    async beforeFileUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2;

      let fileForm = new FormData();

      if (!isLt2M) {
        this.$message.error("上传文件大小不能超过 2MB!");
      }

      fileForm.append("file", file);

      var resp = await fileUpdate(fileForm).catch(() => {
        this.$message.error("文件上传到服务器异常");
      });

      if (Object.prototype.hasOwnProperty.call(resp.data, "message")) {
        this.$message.error(resp.data.message);
      } else {
        this.$message.success("文件上传成功");
      }
      this.editorData += resp.data.path;
    },
    onReady(editor) {
      // 自定义上传图片插件
      editor.plugins.get("FileRepository").createUploadAdapter = (loader) => {
        return new MyUploadAdapter(loader);
      };
    },
  },
};

function RemoveFormatLinks(editor) {
  // Extend the editor schema and mark the "linkHref" model attribute as formatting.
  editor.model.schema.setAttributeProperties("linkHref", {
    isFormatting: true,
  });
}
</script>

<style>
/*编辑框最低高度*/
.ck-editor__editable {
  min-height: 200px;
}
.ck-content .image-style-side {
    max-width: 50%;
    float: right;
    margin-left: var(--ck-image-style-spacing);
}
</style>
