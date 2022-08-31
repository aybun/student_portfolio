const routes=[
    {path:'/home',component:home},
    {path:'/employee',component:employee},
    {path:'/department',component:department}
]

const router=new VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
})

//const app = new Vue({
//    router
//}).$mount('#app')

const app = Vue.createApp({})
app.use(router)
app.mount('#app')