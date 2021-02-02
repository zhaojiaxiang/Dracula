export default {
    routes: [
      {
        path: "/login",
        name: "Login",
        component: () => import("@/pages/Account/Login"),
      },
      {
        path: "/",
        name: "Home",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/Home"),
      },
      {
        path: "/qa",
        name: "Qa",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/Qa"),
      },
      {
        path: "/qa/design_review",
        name: "QaDesignReview",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/QaDesignReview"),
      },
      {
        path: "/qa/testlist",
        name: "QaTestList",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/QaTestList"),
      },
      {
        path: "/qa/pcllist",
        name: "QaPclList",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/QaPclList"),
      },
      {
        path: "/qa/content_text",
        name: "QaContentText",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/QaContectText"),
      },
      {
        path: "/task",
        name: "Task",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/MyTask"),
      },
      {
        path: "/task/release",
        name: "TaskRelease",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/MyTaskRelease"),
      },
      {
        path: "/task/list",
        name: "TaskList",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Home/components/MyTaskList"),
      },
      {
        path: "/project/overview",
        name: "ProjectOverview",
        meta: { requiresAuth: true },
        component: () => import("@/pages/Project/components/ProjectItemOverView"),
      },
      
    ],
    mode: "history",
  };
  