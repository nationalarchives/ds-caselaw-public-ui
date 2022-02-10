const path = require('path');

module.exports = {
  mode: 'development',
  devtool: false,
  entry: './ds_judgements_public_ui/static/js/src/app.js',
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'ds_judgements_public_ui/static/js/dist'),
  },
  module: {
  rules: [
    {
      test: /\.m?js$/,
      exclude: /(node_modules|bower_components)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env']
        }
      }
    }
  ]
}
};
