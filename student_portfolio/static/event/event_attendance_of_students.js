let eventAttendanceComponent = {
    template: '#event-attendance-template',

    data(){
    return{
        // departments:[],
        // students:[],

        modalTitle:"",
        addingNewStudent : false,

        // id:0,
        eventId:0,
        event: 0,


        studentAttendances:[],
        studentId:0,
        newStudentId:"",
        firstname:"",
        middlename:"",
        lastname:"",

        // PhotoFileName:"anonymous.png",
        // PhotoPath:variables.PHOTO_URL
    }
},
methods:{
    refreshData(){
        // this.eventId = this.$route.params.eventId[0] //eventId is an array.
        // this.eventId = this.$parent.params.eventId[0] //eventId is an array.
        // this.eventId = this._routerRoot._router.params.eventId[0]

        this.eventId = JSON.parse(document.getElementById('eventId-data').textContent);

        axios.get(variables.API_URL+"event/"+ this.eventId)
        .then((response)=>{
            this.event=response.data;
        });

        axios.get(variables.API_URL+"eventAttendanceOfStudents/" + this.eventId)
        .then((response)=>{
            this.studentAttendances=response.data;
        });




    },
    addClick(){
        this.modalTitle="Add Student"
        this.addingNewStudent = true // Signal that we are adding a new student -> Create Button.

        this.studentId=0
        this.firstname=""
        this.middlename=""
        this.lastname=""

        // this.DateOfJoining="",
        // this.PhotoFileName="anonymous.png"
    },
    editClick(attendance){
        this.modalTitle="Edit Student";
        this.addingNewStudent = false

        // this.id         =   student.id
        this.eventId    =   attendance.eventId
        this.studentId  =   attendance.studentId
        this.newStudentId = attendance.studentId
        this.firstname  =   attendance.firstname
        this.middlename =   attendance.middlename
        this.lastname   =   attendance.lastname

    },
    createClick(){
        axios.post(variables.API_URL+"eventAttendanceOfStudents/" + this.eventId,{
            'eventId'  :  this.eventId,
            'studentId':  this.studentId,
            'firstname':  this.firstname,
            'middlename': this.middlename,
            'lastname':   this.lastname,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });

    },
    updateClick(){
        axios.put(variables.API_URL+"eventAttendanceOfStudents/"+ this.eventId + "/"+ this.studentId, {
            'eventId'  :    this.eventId,
            'studentId':    this.studentId,
            'newStudentId': this.newStudentId,
            'firstname':    this.firstname,
            'middlename':   this.middlename,
            'lastname':     this.lastname,
            'synced'    :   false,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });
    },
    deleteClick(studentId){
        if(!confirm("Are you sure?")){
            return;
        }

        axios.delete(variables.API_URL+"eventAttendanceOfStudents/"+ this.eventId + '/' + studentId)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });

    },

    syncByStudentIdClick(){
        axios.put(variables.API_URL+"syncStudentAttendanceByStudentId/"+ this.eventId , {
            'eventId': this.eventId,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });
    },
    // imageUpload(event){
    //     let formData=new FormData();
    //     formData.append('file',event.target.files[0]);
    //     axios.post(
    //         variables.API_URL+"employee/savefile",
    //         formData)
    //         .then((response)=>{
    //             this.PhotoFileName=response.data;
    //         });
    // }

},
mounted:function(){
    this.refreshData();

}
}

const app = Vue.createApp({
    components: {'event-attendance-html' : eventAttendanceComponent},
            // this.eventId = this.$route.params.eventId[0] //eventId is an array.

    // data(){
    // return {
    //     eventId : this.$route.params.eventId[0]
    // }
    // }

})

app.mount('#app')