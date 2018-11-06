import Vue from 'vue'
import VueResource from 'vue-resource'
import App from './App'

import './design'

Vue.use(VueResource)

Vue.config.productionTip = false

var app

if (!app) {
  app = new Vue({
    el: '#app',
    data: {toggled: false},
    template: '<App/>',
    components: { App }
  })
}
