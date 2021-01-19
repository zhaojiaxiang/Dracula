import VueRouter from 'vue-router'
import Vue from 'vue'
import config from "./config";

//1、安装
Vue.use(VueRouter)

//2、创建路由对象
var router = new VueRouter(config)

router.beforeEach((to, from, next) => {
    if (to.path === '/login') {
      next();
    } else {
      let token = localStorage.getItem('token');
   
      if (token === 'null' || token === '') {
        next('/login');
      } else {
        next();
      }
    }
  });
   

export default router;