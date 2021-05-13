module.exports = {
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/api': {
				target: 'http://127.0.0.1:5000/', // 接口的域名
        ws: true,
        changeOrigin: true,	
        pathRewrite: {
          '^/api': '/'
        }
			}
    }
    
  }
}