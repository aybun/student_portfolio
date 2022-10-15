
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

            this.event = this.getEmptyEvent()
        },
    addClick(){
        console.log(this.events)
        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.

        this.event = this.getEmptyEvent()
        this.checkboxes=[]
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

        // delete this.event['eventId']
        if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' || this.event.attachment_file === '' )
            delete this.event.attachment_file

        let outDict = new FormData();
        console.log(this.event)
        for (const [key, value] of Object.entries(this.event)) {
            // console.log(key, value);
            outDict.append(key.toString(), value)
        }
        //reassign
        this.event.skills = before_altered_event.skills

        alert(JSON.stringify(outDict, null, 2))

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
    },
    updateClick(){
        //Store only altered fiels.

        this.event.skills = this.cleanSkills(this.event.skills);

        this.event.approved = this.checkboxes.includes('approved')
        this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')


        let outDict = new FormData();
        for (const [key, value] of Object.entries(this.event)) {
            outDict.append(key.toString(), value)
        }
        outDict.set('skills', JSON.stringify(this.event.skills))

        //Make a request.
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: variables.API_URL+"event/" + this.event.eventId,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            // this.refreshData();
            alert(response.data);
            window.location.reload();
        })

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
        return {
            eventId:0,
            title:"",
            date: (new Date()).toISOString().split('T')[0],
            mainStaffId:"",
            info:"",
            skills: [],
            approved:false,
            used_for_calculation: false,
            attachment_link: "",
            attachment_file: "",
        }

    },
    onFileSelected(event){
        this.event.attachment_file = event.target.files[0]

        // let label = document.getElementById("attachment_filename");
        // label.innerText = this.event.attachment_file.name

    },

    prepareData(){
        // this.user['is_staff'] = Object.values(this.user.groups).includes('staff')
        // this.user['is_student'] = Object.values(this.user.groups).includes('student')
        // console.log(this.user)
    }
    },


    created:async function(){
        await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            });

        axios.get(variables.API_URL+"event")
            .then((response)=>{
                this.events=response.data;
                console.log(this.events)
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

    mounted:function(){
        this.refreshData();

    }
}

const app = Vue.createApp({
    components: {'event-html' : eventComponent},

})

app.mount('#app')