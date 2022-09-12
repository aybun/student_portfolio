
let eventComponent = {
    template: '#event-template',

    data(){
        return{
            staffs:[],
            events:[],
            user:{},

            modalTitle:"",
            addingNewEvent : false,

            // id:0,
            event: {
                eventId:0,
                title:"",
                date:"",
                mainStaffId:"",
                info:"",
                skills: [],
                approved:false,
                used_for_calculation: false,
            },


            // is_staff: true,

            skillTable:"",
            checkboxes: [],
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
        document.getElementById("createButton").disabled = false;

        this.event = this.getEmptyEvent()

        this.checkboxes=[]
        // this.DateOfJoining="",
        // this.PhotoFileName="anonymous.png"
    },
    editClick(event){
        this.modalTitle="Edit Event";
        this.addingNewEvent = false

        this.event = event
        this.checkboxes = []


        //Consider create a list of checkbox variables.

        if (event.approved)
            this.checkboxes.push('approved')
        if (event.used_for_calculation)
            this.checkboxes.push('used_for_calculation')

    },
    createClick(){
        this.event.skills = this.cleanSkills(this.event.skills)

        delete this.event['eventId']
        axios.post(variables.API_URL+"event",{
            event : this.event,
        })
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });

        //if success
        //document.getElementById("createButton").disabled = true;

    },
    updateClick(){

        this.event.skills = this.cleanSkills(this.event.skills);
        this.event.approved = this.checkboxes.includes('approved')
        this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')

        outDict = {
           event : this.event,
        }

        if (!this.user['is_staff']){
            delete outDict.event['approved']
            delete outDict.event['used_for_calculation']
        }

        alert(JSON.stringify(outDict, null, 2))

        axios.put(variables.API_URL+"event/" + this.event.eventId, outDict)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });
    },
    deleteClick(eventId){
        if(!confirm("Are you sure?")){
            return;
        }
        axios.delete(variables.API_URL+"event/" + eventId)
        .then((response)=>{
            this.refreshData();
            alert(response.data);
        });

    },
    addSkillClick(){
        this.event.skills.push({
            skillId: '',
        })
    },
    removeSkillClick(){
        this.event.skills.pop()
    },
    cleanSkills(skills){
        //Remove empty or redundant inputs.
        nonEmpty = []
        skillIds = []
        for (i=0;i<skills.length; ++i) {
            id = skills[i]['skillId']

            if ( id !== "" && !skillIds.includes(id)){
                nonEmpty.push(skills[i]);
                skillIds.push(id)
            }
        }
        return nonEmpty
    },

    getEmptyEvent(){

        let event= {
            eventId:0,
            title:"",
            date:"",
            mainStaffId:"",
            info:"",
            skills: [],
            approved:false,
            used_for_calculation: false,
        }

        return event
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
        axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            });
    }
}

const app = Vue.createApp({
    components: {'event-html' : eventComponent},

})

app.mount('#app')