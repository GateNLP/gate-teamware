const path = require('path')
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  // on Windows you might want to set publicPath: "http://127.0.0.1:8080/"
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : "http://0.0.0.0:8080/",
  outputDir: "static",
  indexPath: '../templates/base-vue.html', // Template for django use, relative to outputDir!

  chainWebpack: (config) => {
    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "static/webpack-stats.json" }]);

    config.optimization.splitChunks(false);

    config.resolve.alias.set("__STATIC__", "static");

    config.devServer
      // the first 3 lines of the following code have been added to the configuration
      .public("http://0.0.0.0:8080")
      .host("0.0.0.0")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["*"] })
      .writeToDisk(filePath => filePath.endsWith('index.html'));
  },

};

