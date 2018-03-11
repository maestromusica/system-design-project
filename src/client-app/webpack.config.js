const path = require('path');
const appPath = path.join(__dirname, 'app/index.js')

module.exports = {
  entry: appPath,
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  },
  target: 'web'
}
