import VueRouter from "vue-router";
import Vue from "vue";
import config from "./config";
import { isLogin } from "../utils/auth";

//1、安装
Vue.use(VueRouter);

//2、创建路由对象
var router = new VueRouter(config);

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
  return originalPush.call(this, location).catch(err => err)
}

// 路由判断登录 根据路由配置文件的参数
router.beforeEach(async(to, from, next) => {
  var islogin = await isLogin()
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // 判断该路由是否需要登录权限
    if (islogin === true) {
      next();
    } else {
      next({
        path: "/login",
        query: { redirect: to.fullPath }, // 将跳转的路由path作为参数，登录成功后跳转到该路由
      });
    }
  } else {
    next();
  }
});

export default router;
