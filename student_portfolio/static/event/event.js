
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
                attachment_link: "",
                attachment_file: "",
            },


            // is_staff: true,

            skillTable:"",
            checkboxes: [],
            // PhotoFileName:"anonymous.png",
            PhotoPath:variables.PHOTO_URL
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

            this.event = this.getEmptyEvent()
        },
    addClick(){

        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.
        // document.getElementById("createButton").disabled = false;

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
        let before_altered_event = this.getEmptyEvent()

        this.event.skills = this.cleanSkills(this.event.skills);
        before_altered_event.skills = this.event.skills

        this.event.skills = JSON.stringify(this.event.skills)

        delete this.event['eventId']
        if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' || this.event.attachment_file === '' )
            delete this.event.attachment_file

        let outDict = new FormData();
        console.log(this.event)
        for (const [key, value] of Object.entries(this.event)) {
            // console.log(key, value);
            outDict.append(key.toString(), value)
        }

        alert(JSON.stringify(outDict, null, 2))

        // axios.post(variables.API_URL+"event", outDict,
        //     { headers: {'Content-Type': 'multipart/form-data'}})
        //     .then((response)=>{
        //     this.refreshData();
        //     alert(response.data);
        // });

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'post',
            url: variables.API_URL+"event",
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


        //if success
        //document.getElementById("createButton").disabled = true;

        this.event.skills = before_altered_event.skills
    },
    updateClick(){
        //Store only altered fiels.
        let before_altered_event = this.getEmptyEvent()

        this.event.skills = this.cleanSkills(this.event.skills);
        before_altered_event.skills = this.event.skills

        this.event.approved = this.checkboxes.includes('approved')
        this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')

        if (!this.user['is_staff']){
            delete this.event['approved']
            delete this.event['used_for_calculation']
        }

        if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' )
            delete this.event.attachment_file


        this.event.skills = JSON.stringify(this.event.skills)
        alert(JSON.stringify(this.event, null, 2))
        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.event)) {
            outDict.append(key.toString(), value)
        }

        //Make a request.
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"event/" + this.event.eventId,
            xstfCookieName: 'csrftoken',
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

        //Assign some values back.
        this.event.skills = before_altered_event.skills
    },
    deleteClick(eventId){
        if(!confirm("Are you sure?")){
            return;
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"event/"+ eventId,
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
            attachment_link: "",
            attachment_file: "",
        }

        return event
    },
    onFileSelected(event){
        this.event.attachment_file = event.target.files[0]

        let label = document.getElementById("attachment_filename");
        label.innerText = this.event.attachment_file.name

    },
        cleanAttachment_file(attachement_file){

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
    components: {'event-html' : eventComponent},

})

app.mount('#app')