import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import Award from "../components/award/Award.vue";
import Login from "../components/registration/Login.vue";
import Event from "../components/event/Event.vue";
import Project from "/src/components/project/Project.vue"

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/award",
      name: "award",
      component: Award,  
    },
    {
      path: "/login-vue",
      name: "login-vue",
      component: Login,  
    },
    {
      path: "/event",
      name: "event",
      component: Event,  
    },
    {
      path: "/project",
      name: "project",
      component: Project,  
    },


  ],
});

export default router;
