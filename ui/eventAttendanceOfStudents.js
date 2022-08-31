const eventAttendanceOfStudents={template:`
<div>


<table class="table table-striped">
<thead>
    <tr>
        <th>
            Event Id
        </th>
        <th>
            Title
        </th>
        <th>
            Date
        </th>
        <th>
            Main Staff Id
        </th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>{{event.eventId}}</td>
        <td>{{event.title}}</td>
        <td>{{event.date}}</td>
        <td>{{event.mainStaffId}}</td>
    </tr>
</tbody>
</thead>
</table>

<button type="button"
class="btn btn-primary m-2 fload-end"
data-bs-toggle="modal"
data-bs-target="#exampleModal"
@click="addClick()">
 Add Student to The Event
</button>

<button type="button"
class="btn btn-primary m-2 fload-end"

@click="syncByStudentIdClick()">
 Sync by StudentId
</button>

<table class="table table-striped">
<thead>
    <tr>
        <th>
            Student Id
        </th>
        <th>
            Firstname
        </th>
        <th>
            Middlename
        </th>
        <th>
            Lastname
        </th>
        
        <th>
            Synced
        </th>
        <th>
            Options
        </th>
    </tr>
</thead>
<tbody>
    <tr v-for="att in studentAttendances">
        <td>{{att.studentId}}</td>
        <td>{{att.firstname}}</td>
        <td>{{att.middlename}}</td>
        <td>{{att.lastname}}</td>
        <td>{{att.synced}}</td>
        <td>
            <button type="button"
            class="btn btn-light mr-1"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            @click="editClick(att)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
            </button>
            <button type="button" 
            @click="deleteClick(att.studentId)"
            class="btn btn-light mr-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </button>

        </td>
    </tr>
</tbody>
</thead>
</table>

<div class="modal fade" id="exampleModal" tabindex="-1"
    aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog modal-lg modal-dialog-centered">
<div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">{{modalTitle}}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"
        aria-label="Close"></button>
    </div>

    <div class="modal-body">
    <div class="d-flex flex-row bd-highlight mb-3">
        <div class="p-2 w-50 bd-highlight">

            <div class="input-group mb-3" >
                <span class="input-group-text">Student Id</span>
                <input v-bind:disabled="!addingNewStudent" type="text" class="form-control" v-model="studentId">
            </div>

            <div class="input-group mb-3" v-if="!addingNewStudent">
                <span class="input-group-text">New Id</span>
                <input type="text" class="form-control" v-model="newStudentId">
            </div>

            <div class="input-group mb-3">
                <span class="input-group-text">Firstname</span>
                <input type="text" class="form-control" v-model="firstname">
            </div>

            <div class="input-group mb-3">
                <span class="input-group-text">Middlename</span>
                <input type="text" class="form-control" v-model="middlename">
            </div>

            <div class="input-group mb-3">
                <span class="input-group-text">Lastname</span>
                <input type="text" class="form-control" v-model="lastname">
            </div>
            

            <!--
            <div class="input-group mb-3">
                <span class="input-group-text">Department</span>
                <select class="form-select" v-model="Department">
                    <option v-for="dep in departments">
                    {{dep.DepartmentName}}
                    </option>
                </select>
            </div>
            -->

            <!--
            <div class="input-group mb-3">
                <span class="input-group-text">DOJ</span>
                <input type="date" class="form-control" v-model="DateOfJoining">
            </div>
            -->

        </div>

        <!--
        <div class="p-2 w-50 bd-highlight">
            <img  
                :src="PhotoPath+PhotoFileName" />
            <input class="m-2" type="file" @change="imageUpload">
        </div> 
        -->
        
    </div>
        <button type="button" @click="createClick()"
        v-if="addingNewStudent" class="btn btn-primary">
        Create
        </button>
        <button type="button" @click="updateClick()"
        v-else class="btn btn-primary">
        Update
        </button>

    </div>

</div>
</div>
</div>


</div>


`,

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
        this.eventId = this.$route.params.eventId[0] //eventId is an array. 
        
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

        axios.delete(variables.API_URL+"eventAttendanceOfStudents/"+ this.eventId + "/" + studentId)
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