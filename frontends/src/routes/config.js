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
        component: () => import("@/pages/Home/Home"),
      },
      {
        path: "/qa",
        name: "Qa",
        component: () => import("@/pages/Home/components/Qa"),
      },
      {
        path: "/qa/design_review",
        name: "QaDesignReview",
        component: () => import("@/pages/Home/components/QaDesignReview"),
      },
      {
        path: "/qa/testlist",
        name: "QaTestList",
        component: () => import("@/pages/Home/components/QaTestList"),
      },
      
    ],
    mode: "history",
  };
  