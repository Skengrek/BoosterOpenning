const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    allowedHosts: [
      'localhost',
      'skengrek.fr',
      '192.168.1.1',
    ],
  },
};
