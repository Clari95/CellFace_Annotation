module.exports = {
  transpileDependencies: [
    'vuetify',
  ],
  devServer: {
    disableHostCheck: true, // NOT safe for production
    proxy: 'http://127.0.0.1:8081/', 
  },
};
