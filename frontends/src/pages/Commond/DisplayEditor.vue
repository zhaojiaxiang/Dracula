<template>
  <div>
    <el-row>
      <el-col style="margin-top:15px">
        <ckeditor
          id="editor"
          @ready="onReady"
          :editor="editor"
          :value="content_text"
          :config="editorConfig"
        ></ckeditor>
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

export default {
  components: {
    // Use the <ckeditor> component in this view.
    ckeditor: CKEditor.component,
  },
  props: ["content_text"],
  data() {
    return {
      activeNames: [0],
      editor: ClassicEditor,
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
      },
    };
  },
  methods: {
    onReady(editor) {
      editor.isReadOnly = true;
    },
  },
};
</script>

<style></style>
