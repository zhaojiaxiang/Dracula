const path = require("path");
const CKEditorWebpackPlugin = require("@ckeditor/ckeditor5-dev-webpack-plugin");
const { styles } = require("@ckeditor/ckeditor5-dev-utils");
// const targetUrl = "http://47.254.42.122/"
const targetUrl = "http://127.0.0.1:8000/"

module.exports = {
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    disableHostCheck: true,
    proxy: {
      "/api": {
        target: targetUrl,
        changeOrigin: true,
        pathRewrite: {
          "^/api": "/api",
        },
      },
      "/media": {
        target: targetUrl,
        changeOrigin: true,
        pathRewrite: {
          "^/media": "/media",
        },
      },
      "/qa/files": {
        target: targetUrl,
        changeOrigin: true,
        pathRewrite: {
          "^/qa/files": "/api/files",
        },
      },
      "/files": {
        target: targetUrl,
        changeOrigin: true,
        pathRewrite: {
          "^/files": "/api/files",
        },
      },
    },
    // build: {
    //   // Template for index.html
    //   index: path.resolve(__dirname, "../dist/index.html"),

    //   // Paths
    //   assetsRoot: path.resolve(__dirname, "../dist"),
    //   assetsSubDirectory: "static",
    //   assetsPublicPath: "./",
    // },
  },

  // The source of CKEditor is encapsulated in ES6 modules. By default, the code
  // from the node_modules directory is not transpiled, so you must explicitly tell
  // the CLI tools to transpile JavaScript files in all ckeditor5-* modules.
  transpileDependencies: [/ckeditor5-[^/\\]+[/\\]src[/\\].+\.js$/],

  configureWebpack: {
    plugins: [
      // CKEditor needs its own plugin to be built using webpack.
      new CKEditorWebpackPlugin({
        // See https://ckeditor.com/docs/ckeditor5/latest/features/ui-language.html
        language: "en",

        // Append translations to the file matching the `app` name.
        translationsOutputFile: /app/,
      }),
    ],
  },

  // Vue CLI would normally use its own loader to load .svg and .css files, however:
  //	1. The icons used by CKEditor must be loaded using raw-loader,
  //	2. The CSS used by CKEditor must be transpiled using PostCSS to load properly.
  chainWebpack: (config) => {
    // (1.) To handle editor icons, get the default rule for *.svg files first:
    const svgRule = config.module.rule("svg");

    // Then you can either:
    //
    // * clear all loaders for existing 'svg' rule:
    //
    //		svgRule.uses.clear();
    //
    // * or exclude ckeditor directory from node_modules:
    svgRule.exclude.add(path.join(__dirname, "node_modules", "@ckeditor"));

    // Add an entry for *.svg files belonging to CKEditor. You can either:
    //
    // * modify the existing 'svg' rule:
    //
    //		svgRule.use( 'raw-loader' ).loader( 'raw-loader' );
    //
    // * or add a new one:
    config.module
      .rule("cke-svg")
      .test(/ckeditor5-[^/\\]+[/\\]theme[/\\]icons[/\\][^/\\]+\.svg$/)
      .use("raw-loader")
      .loader("raw-loader");

    // (2.) Transpile the .css files imported by the editor using PostCSS.
    // Make sure only the CSS belonging to ckeditor5-* packages is processed this way.
    config.module
      .rule("cke-css")
      .test(/ckeditor5-[^/\\]+[/\\].+\.css$/)
      .use("postcss-loader")
      .loader("postcss-loader")
      .tap(() => {
        return styles.getPostCssConfig({
          themeImporter: {
            themePath: require.resolve("@ckeditor/ckeditor5-theme-lark"),
          },
          minify: true,
        });
      });
  },
};
