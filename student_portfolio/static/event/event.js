
let eventComponent = {
    template: '#event-template',

    data(){
        return{
            staffs:[],
            events:[],
            user:{},

            modalTitle:"",
            addingNewEvent : false,
            showApproved: true,

            // id:0,
            event: {},


            // is_staff: true,

            skillTable:"",
            checkboxes: [],
            // skills:{},
            // PhotoFileName:"anonymous.png",

            PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        refreshData(){
            axios.get(variables.API_URL+"event")
            .then((response)=>{
                this.events=response.data;
                console.log(this.events)
            });

        },

    addClick(){
        console.log(this.events)
        this.modalTitle="Add Event"
        this.addingNewEvent= true // Signal that we are adding a new event -> Create Button.

        this.event = this.getEmptyEvent()
        this.checkboxes=[]
    },

    editClick(event){

        console.log(event);
        this.modalTitle="Edit Event";
        this.addingNewEvent = false

        this.event = event
        // this.event.skills = []

        this.checkboxes = []

        //Consider create a list of checkbox variables.
        if (event.approved)
            this.checkboxes.push('approved')
        if (event.used_for_calculation)
            this.checkboxes.push('used_for_calculation')

    },
    createClick(){

        // this.event.skills = this.cleanSkills(this.event.skills);
        // let skillIds = this.getSkillIds(this.event.skills)

        // delete this.event['eventId']
        // if (this.event.attachment_file == null || typeof this.event.attachment_file === 'string' || this.event.attachment_file === '' )
        //     delete this.event.attachment_file

        let outDict = new FormData();
        console.log(this.event)
        for (const [key, value] of Object.entries(this.event)) {
            // console.log(key, value);
            outDict.append(key.toString(), value)
        }

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
        // console.log(this.event.skills)
        this.event.skills = this.cleanSkills(this.event.skills);

        this.event.approved = this.checkboxes.includes('approved')
        this.event.used_for_calculation = this.checkboxes.includes('used_for_calculation')

        console.log(this.event)
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
            url: variables.API_URL+"event/" + this.event.id,
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
            // window.location.reload();
        })

    },
    deleteClick(event_id){
        if(!confirm("Are you sure?")){
            return;
        }
        console.log(event_id)
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'delete',
            url: variables.API_URL+"event/"+ event_id,
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
            id: '',
        })
    },
    removeSkillClick(){
        this.event.skills.pop()
    },
    cleanSkills(skills){
        //Remove empty or redundant inputs.
        nonEmpty = []
        skillIds = []
        for (let i=0;i<skills.length; ++i) {
            id = skills[i]['id']

            if ( id !== "" && !skillIds.includes(id)){
                skillIds.push(skills[i].id);
                nonEmpty.push(skills[i])

                // for (let j=0; j < this.skillTable.length; ++j){
                //     if (id === this.skillTable[j].id)
                //         nonEmpty.push(this.skillTable[j])
                // }
            }
        }
        return nonEmpty
    },
    getSkillIds(){
        // nonEmpty = []
        skillIds = []
        for (i=0;i<skills.length; ++i) {
            id = skills[i]['id']

            if ( id !== "" && !skillIds.includes(id)){
                // nonEmpty.push(skills[i]);
                skillIds.push(id)
            }
        }
        return skillIds
    },

    getEmptyEvent(){
        return {
            id:0,
            title:"",
            start_datetime: (new Date()).toLocaleString(),
            end_datetime: (new Date()).toLocaleString(),
            info:"",

            created_by:"",
            approved:false,
            approved_by:"",
            used_for_calculation: false,
            arranged_inside: false,
            attachment_link: "",
            attachment_file: "",

            //Additional data.
            skills: [],
        }

    },
    onFileSelected(event){
        this.event.attachment_file = event.target.files[0]

        // let label = document.getElementById("attachment_filename");
        // label.innerText = this.event.attachment_file.name

    },
    openNewWindow(url){
            window.open(url);

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
        this.event = this.getEmptyEvent()

    }
}

const app = Vue.createApp({
    components: {'event-html' : eventComponent},

})

app.mount('#app')