const {createProxyMiddleware} = require('http-proxy-middleware')

module.exports = function (app) {
    
    app.use(createProxyMiddleware('/predict', {  
      target: 'http://127.0.0.1:5000', 
      changeOrigin: true
  }))

  app.use(createProxyMiddleware('/getfinish', {  
    target: 'http://127.0.0.1:5000', 
    changeOrigin: true
}))

app.use(createProxyMiddleware('/cancel_task', {  
  target: 'http://127.0.0.1:5000', 
  changeOrigin: true
}))
}
