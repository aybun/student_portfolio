import Vue from "vue";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

// import bootstrap from 'bootstrap'
// import "../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
// import "../node_modules/bootstrap/dist/css/bootstrap.min.css"

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
