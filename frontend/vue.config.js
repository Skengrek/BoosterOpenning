const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    host: '0.0.0.0',  // Bind to all network interfaces
    port: 8080,        // Ensure this matches your container’s internal port
    public: 'skengrek.fr',  // Set the public URL
    disableHostCheck: true, // Disable host header checks (optional)
  }
}