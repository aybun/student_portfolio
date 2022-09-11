
let eventRegisterRequestComponent = {
    template: '#event-register-request-template',

    data(){
        return{
            user:"",

            staffs:[],
            events:[],

            modalTitle:"",
            addingNewEvent : false,

            // id:0,
            eventId:0,
            title:"",
            date:"",
            mainStaffId:"",
            info:"",

            is_staff: false,

            skillTable:"",
            skills: [],

            checkboxes :[],

            // PhotoFileName:"anonymous.png",
            // PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        refreshData(){
            this.is_staff = JSON.parse(document.getElementById('is_staff-data').textContent);

            axios.get(variables.API_URL+"eventRegisterRequest")
            .then((response)=>{
                this.events=response.data;
            });

            axios.get(variables.API_URL+"staff")
            .then((response)=>{
                this.staffs=response.data;
            });

            axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
            });


        },
    addClick(){

        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.
        document.getElementById("createButton").disabled = false;

        // this.eventId=0
        this.title=""
        this.date=""
        this.mainStaffId=""
        this.info="-" // Add some thing to the field.
        this.skills = []
        this.checkboxes = []
        // this.DateOfJoining="",
        // this.PhotoFileName="anonymous.png"
    },
    editClick(event){
        this.modalTitle="Edit Event";
        this.addingNewEvent = false

        // this.id         =   event.id
        this.eventId        =   event.eventId
        this.title          =   event.title
        this.date           =   event.date
        this.mainStaffId    =   event.mainStaffId
        this.info           =   event.info
        this.skills         =   event.skills
        // this.approved       =   event.approved
        // this.used_for_calculation = event.used_for_calculation

        this.checkboxes = []
        if (event.approved)
            this.checkboxes.push('approved')
        if (event.used_for_calculation)
            this.checkboxes.push('used_for_calculation')


    },
    createClick(){
        responseData=""

        this.skills = this.cleanSkills(this.skills)
        axios.post(variables.API_URL+"eventRegisterRequest",{
            // eventId:    this.eventId,
            'title':      this.title,
            'date':       this.date,
            'mainStaffId':this.mainStaffId,
            'info':       this.info,
            'skills':     this.skills,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
            responseData = response.data
        });

        // check if successfully added.
        // if responseData =
        // document.getElementById("createButton").disabled = true;

    },
    updateClick(){

        this.skills = this.cleanSkills(this.skills);
        const tempOutData = {
            'skills' : this.skills
        }
        alert(JSON.stringify(tempOutData, null, 2))

        outDict = {
            // id:         this.id,
            'eventId':    this.eventId,
            'title':      this.title,
            'date':       this.date,
            'mainStaffId':this.mainStaffId,
            'info':       this.info,
            'skills':     this.skills,
            'approved':   this.checkboxes.includes('approved'),
            'used_for_calculation': this.checkboxes.includes('used_for_calculation'),
        }

        if (!this.user['is_staff']){
            outDict.delete('approved')
            outDict.delete('used_for_calculation')
        }

        axios.put(variables.API_URL+"eventRegisterRequest/" + this.eventId, outDict)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });
    },
    deleteClick(eventId){
        if(!confirm("Are you sure?")){
            return;
        }
        axios.delete(variables.API_URL+"event/"+eventId)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });

    },
    addSkillClick(){
            this.skills.push({
                skillId: '',
            })
    },
    removeSkillClick(){
            this.skills.pop()
    },
    cleanSkills(skills){
        //Remove empty or redundant inputs.
        nonEmpty = []
        skillIds = []
        for (i=0;i<skills.length; ++i) {
            id = this.skills[i]['skillId']

            if ( id !== "" && !skillIds.includes(id)){
                nonEmpty.push(skills[i]);
                skillIds.push(id)
            }
        }
        return nonEmpty
    }

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

        axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            });


    }
}

const app = Vue.createApp({
    components: {'event-register-request-html' : eventRegisterRequestComponent},


})

app.mount('#app')