const routes=[
    {path:'/home',component:home},
    {path:'/student',component:student},
    {path:'/staff',component:staff},
    {path:'/event',component:event},
    {path:'/eventAttendanceOfStudents/:eventId(\\d+)+', component:eventAttendanceOfStudents}
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