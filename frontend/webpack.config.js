var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {
        app: './src/assets/main',
        css: './src/assets/css',
    },
    output: {
        path: path.resolve('./src/assets/bundles/'),
        filename: "[name]-[hash].js",
    },

    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' })
    ]
}