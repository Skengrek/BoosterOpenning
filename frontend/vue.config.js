const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
    disableHostCheck: true,  // Disables host header checking
    port: 8080,              // Ensure this matches your container's internal port
    public: 'skengrek.fr',   // Public-facing address (optional)
    allowedHosts: [
      '.skengrek.fr'         // Allow your domain
    ]
  };
