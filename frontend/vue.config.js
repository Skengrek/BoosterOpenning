const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: '/collection',
  transpileDependencies: true,
    devServer: {
      allowedHosts: [
        'skengrek.fr'
      ]
  }
})