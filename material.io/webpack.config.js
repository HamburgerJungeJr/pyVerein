const autoprefixer = require('autoprefixer');

module.exports = [{
    entry: './sass/material.scss',
    output: {
      // This is necessary for webpack to compile
      // But we never use style-bundle.js
      filename: 'style-bundle.js',
    },
    module: {
      rules: [{
        test: /\.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '../pyVerein/app/static/app/css/material.css',
            },
          },
          { loader: 'extract-loader' },
          { loader: 'css-loader' },
          { 
            loader: 'postcss-loader',
            options: {
              plugins: () => [autoprefixer({ grid: false })]
            }
          }, 
          { 
            loader: 'sass-loader',
            options: {
              includePaths: ['./node_modules']
            } 
          },
        ]
      }]
    },
  },
  {
    entry: './js/material.js',
    output: {
      filename: '../pyVerein/app/static/app/js/material.js'
    },
    module: {
      loaders: [{
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015']
        }
      }]
    },
  },
  {
    entry: './sass/app.scss',
    output: {
      // This is necessary for webpack to compile
      // But we never use style-bundle.js
      filename: 'style-bundle.js',
    },
    module: {
      rules: [{
        test: /\.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '../pyVerein/app/static/app/css/app.css',
            },
          },
          { loader: 'extract-loader' },
          { loader: 'css-loader' },
          { 
            loader: 'postcss-loader',
            options: {
              plugins: () => [autoprefixer({ grid: false })]
            }
          }, 
          { 
            loader: 'sass-loader',
            options: {
              includePaths: ['./node_modules']
            } 
          },
        ]
      }]
    },
  },];