
let chartComponent = {
    template: '#chart-template',

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

            skillLabels:[],
            skillTable:"",
            skillFreq:[],

            radarChart:{},

            checkboxes: [],
            // PhotoFileName:"anonymous.png",
            PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        async refreshData(){


            this.reloadCharts()

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

        },

        submitChartDataClick(){

            this.radarChart.destroy()
            this.reloadCharts()

            let outDict = JSON.parse(JSON.stringify(this.skillTable))
            console.log(outDict)
            console.log(this.skillTable)
            for (let i = 0; i < this.skillTable.length ;++i){
                outDict[i].goal_point = this.skillFreq[i]
            }
            console.log(outDict)

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"skillTable",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers : {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                alert(response.data);
            })
            //push to DB.
        },
        reloadCharts(){

            //Process Data
            //Handle the case where the ids of skills do not start with 1.
            let chartContainer = document.getElementById('chart-inputs')
            if (this.user.is_student)
                chartContainer.style.visibility = "hidden"

            const ctx = document.getElementById('myChart').getContext('2d');


            const chart_data = {

                labels: this.skillLabels,
                datasets: [{
                    label: 'My Skills',
                    data: this.skillFreq,
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                },
                ]
            };

            if (this.user.is_staff){
                chart_data.datasets[0] = {
                    label: 'Goal',
                    data: this.skillFreq,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }
            }

            if (this.user.is_student){

                let goalFreq = []
                for (let i=0; i < this.skillTable.length; ++i){
                    goalFreq.push(this.skillTable[i].goal_point)
                }

                goalData = {
                    label: 'Goal',
                    data: goalFreq,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
              }

                chart_data.datasets.push(goalData)

            }


            const config = {
                type: 'radar',
                data: chart_data,
                options: {
                    // responsive: false,
                    // maintainAspectRatio: false,
                    scales:{
                        r:{
                            max:5,
                            min:0,
                        },
                    },

                    elements: {
                        line: {
                            borderWidth: 3
                        }
                }
              },
            };
            this.radarChart = new Chart(ctx, config);
        },

        prepareChartData(){
            //Initialize skillFreq
            if (this.user.is_student){

                let skillFreq = {}
                for (let i=0; i<this.skillTable.length; ++i){
                    skillFreq[this.skillTable[i].skillId] = 0
                }
                for (let i=0; i < this.events.length; ++i){
                    for (let j=0; j < this.events[i].skills.length; ++j){
                        skillFreq[this.events[i].skills[j].skillId] += 1
                    }
                }
                let temp_skillFreq = []
                for (let i=0; i < this.skillTable.length; ++i){
                    temp_skillFreq.push(skillFreq[this.skillTable[i].skillId])
                }
                this.skillFreq = temp_skillFreq
            }
            else if (this.user.is_staff){
                //query from DB
                let skillFreq = {}
                for (let i=0; i<this.skillTable.length; ++i){
                    skillFreq[this.skillTable[i].skillId] = this.skillTable[i].goal_point
                }

                let temp_skillFreq = []
                for (let i=0; i < this.skillTable.length; ++i){
                    temp_skillFreq.push(skillFreq[this.skillTable[i].skillId])
                }

                this.skillFreq = temp_skillFreq
            }

            //Initialize skillLabels
            let skillLabels = []
            this.skillTable.forEach(function(e) {
                    skillLabels.push(e.title)
                }
            )
            this.skillLabels = skillLabels

        },

        prepareData(){
            console.log(this.user)
            this.user['is_staff'] = Object.values(this.user.groups).includes('staff')
            this.user['is_student'] = Object.values(this.user.groups).includes('student')

            //Prepare chartData depends on the group of the user.
            this.prepareChartData()

            // console.log(typeof this.user.groups)

            // console.log(this.user)
        },
        async makeRequests(){
            await axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
            });

            await axios.get(variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;

            });

            await axios.get(variables.API_URL+"event")
                .then((response)=>{
                    this.events=response.data;
                });

            await axios.get(variables.API_URL+"staff")
                .then((response)=>{
                    this.staffs=response.data;
                });
        }
    },
    created:async function(){

        await this.makeRequests()
        this.prepareData()
        this.refreshData()
    },

    mounted:function(){

    }
}
const app = Vue.createApp({
    components: {
        'chart-html' : chartComponent,
        // 'goal-chart-html' : goalChartComponent,
    },
    data(){
        return {
            user:{},
        }
    },
    created: function(){
        axios.get(variables.API_URL+"user")
        .then((response)=>{
            this.user=response.data;
        });
    },

    mounted: async function(){

    }

})

app.mount('#app')




