const path = require('path');

module.exports = {
    mode: 'none',
    entry: path.resolve(__dirname, 'main4.js'),
    output: {
		libraryTarget: 'commonjs',
        filename: 'builtMain.js',
        path: path.resolve(__dirname, 'build')
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'resolve-url-loader',
                    {
                        'loader': 'sass-loader',
                        options: { sourceMap: true }
                    }
                ]
            }
        ]
    },
    resolve: {
        modules: [
            path.resolve(__dirname, 'style.scss'),
            path.resolve(__dirname, 'node_modules'),
        ]
    },
    watchOptions: {
        ignored: /node_modules/
    },
    devtool: 'eval-source-map',
    stats: 'errors-only'
};
