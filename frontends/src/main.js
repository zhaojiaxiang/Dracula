import Vue from 'vue'
import {BootstrapVue, IconsPlugin  }  from 'bootstrap-vue'
import ElementUI from 'element-ui'
import CKEditor from '@ckeditor/ckeditor5-vue2'
import 'element-ui/lib/theme-chalk/index.css';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.min.css'
import App from './App.vue'
import router from './routes/index';

Vue.config.productionTip = false

Vue.prototype.bus = new Vue()

Vue.use(ElementUI);
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(CKEditor)

new Vue({
  render: function (h) { return h(App) },
  router,   //配置路由到vue实例中
}).$mount('#app')
