let eventAttendanceComponent = {
    template: '#event-attendance-template',

    data(){
        return{
            modalTitle:"",
            addingNewStudent : false,

            studentAttendEvent : {},
            event_id:0,
            // id:0,
            // eventId:0,
            // event: 0,


            studentAttendances:[],
            // studentId:0,
            // newStudentId:"",
            // firstname:"",
            // middlename:"",
            // lastname:"",
            checkboxes:[],
            checkboxFields:['used_for_calculation']
        }
    },

methods:{
    getEmptyStudentAttendEvent(){
            return {
                id:0,
                event_id_fk:'',
                student_id: '',

                firstname:'',
                middlename:'',
                lastname:'',

                student_id_fk:'',
                synced:false,

                used_for_calculation: false,
            }
        },

    refreshData(){
        axios.get(variables.API_URL+"eventAttendanceOfStudents/" + this.event_id)
        .then((response)=>{
            this.studentAttendances=response.data;
        });

    },
    addClick(){
        this.modalTitle="Add Student"
        this.addingNewStudent = true // Signal that we are adding a new student -> Create Button.

        this.studentAttendEvent = this.getEmptyStudentAttendEvent()

    },
    editClick(attendance){
        this.modalTitle="Edit Student";
        this.addingNewStudent = false

        this.studentAttendEvent = attendance
        this.checkboxes = []

        for(let i=0; i < this.checkboxFields.length; ++i){
            if (this.studentAttendEvent[this.checkboxFields[i]])
                this.checkboxes.push(this.checkboxFields[i])
        }

    },
    createClick(){

        for (let i =0 ; i < this.checkboxFields.length; ++i)
            this.studentAttendEvent[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.studentAttendEvent)) {
            outDict.append(key.toString(), value)
        }
        outDict.set('event_id_fk', this.event_id)

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'post',
            url: variables.API_URL+"eventAttendanceOfStudents/",
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            alert(response.data);
        })

    },
    updateClick(){

        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.studentAttendEvent)) {
            outDict.append(key.toString(), value)
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"eventAttendanceOfStudents/" + this.event_id + '/' + this.studentAttendEvent.id,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            alert(response.data);
        })
    },

    deleteClick(attendance_id){
        if(!confirm("Are you sure?")){
            return;
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"eventAttendanceOfStudents/"+ this.event_id + '/' + attendance_id,
            xstfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            headers : {
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.refreshData();
            alert(response.data);
        })
    },

    syncByStudentIdClick(){
        axios.put(variables.API_URL+"syncStudentAttendanceByStudentId/"+ this.event_id , {
            'eventId': this.eventId,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });
    },

    },

created: function(){


},

mounted:function(){

    this.event_id = JSON.parse(document.getElementById('event_id-data').textContent);
    console.log(this.event_id)
    this.refreshData()


},

}

const app = Vue.createApp({
    components: {'event-attendance-html' : eventAttendanceComponent},

})

app.mount('#app')