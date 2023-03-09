import Vue from "vue";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

import * as VeeValidate from 'vee-validate' 
import VueFormulate from '@braid/vue-formulate'
import axios from 'axios'
import VueCookies from 'vue-cookies'



Vue.use(VeeValidate, {
  errorBagName: 'veeErrors', 
})

Vue.use(VueFormulate)
Vue.prototype.$API_URL = "http://127.0.0.1:8000/api/"

Vue.use(VueCookies)

new Vue({
  router,
  render: (h) => h(App),

  created: function () {
    axios.get(this.$API_URL + 'get-csrf').then((response)=>{
      console.log(response, response.headers['x-csrftoken'])
      this.$cookies.set("x-csrftoken", response.headers['x-csrftoken'], "1d")
      // console.log(this.$cookies.get('x-csrftoken'))
    })

  },

  mounted : function (){
    
  },

}).$mount("#app");
