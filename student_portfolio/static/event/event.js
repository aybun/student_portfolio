
let eventComponent = {
    template: '#event-template',

    data(){
        return{
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

            // is_staff: true,

            skillTable:"",
            skills: [],
            // PhotoFileName:"anonymous.png",
            // PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        refreshData(){
            axios.get(variables.API_URL+"event")
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

        // this.eventId=0
        this.title=""
        this.date=""
        this.mainStaffId=""
        this.info="-" // Add some thing to the field.
        this.skills = []
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
    },
    createClick(){
        axios.post(variables.API_URL+"event",{
            // eventId:    this.eventId,
            title:      this.title,
            date:       this.date,
            mainStaffId:this.mainStaffId,
            info:       this.info
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });


    },
    updateClick(){

        const tempSkills = {
            'skills' : this.skills
        }

        alert(JSON.stringify(tempSkills, null, 2))


        axios.put(variables.API_URL+"event/" + this.eventId,{
            // id:         this.id,
            'eventId':    this.eventId,
            'title':      this.title,
            'date':       this.date,
            'mainStaffId':this.mainStaffId,
            'info':       this.info,
            'skills':     this.skills,
        })
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
    components: {'event-html' : eventComponent},


})

app.mount('#app')