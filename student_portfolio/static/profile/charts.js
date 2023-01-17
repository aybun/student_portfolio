
let chartComponent = {
    template: '#chart-template',

    data(){
        return{
            //API Zone
            user:{},
            profile:{}, //Get Curriculum id
            curriculums:[],
            skillgroups:[],
            skillTable:[],
            events:[],



            // JS editing zone
            modalTitle:"Edit goal points",

            skillFreq:[],
            skillLabels:[],

            radarCharts:[],
            checkboxes: [],

            editingSkillType:0,
            // PhotoFileName:"anonymous.png",
            PhotoPath:variables.PHOTO_URL
        }
    },

    methods:{
        async refreshData(){

            this.reloadCharts()

        },

        editGoalPoints(skillType){
            this.editingSkillType = skillType
        },
        cleanAttachment_file(attachement_file){

        },

        submitChartDataClick(){

            for (let i=0; i<this.radarcharts.length; ++i){
                this.radarcharts[i].destroy()
            }
            this.reloadCharts()

            let outDict = JSON.parse(JSON.stringify(this.skillTable))

            for (let i = 0; i < this.skillTable.length ;++i){
                outDict[i].goal_point = this.skillFreq[i]
            }


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

        getEmptyArrayOfArrays(arrayLength){
            let arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i ){
                arr[i] = []
            }

            return arr
        },
        reloadCharts(){
             //Prepare chartFreqData for each chart.
            let n_types = 2
            this.radarcharts = []
            let chart_freq_data = this.getEmptyArrayOfArrays(n_types)
            let goal_freq_data = this.getEmptyArrayOfArrays(n_types)
            let skill_label_data = this.getEmptyArrayOfArrays(n_types)


            for (let i = 0; i < this.skillTable.length; ++i){
                for (let j = 0; j < n_types; ++j){
                    if (this.skillTable[i].type === (j+1)){
                        chart_freq_data[j].push(this.skillFreq[i])
                        goal_freq_data[j].push(this.skillTable[i].goal_point)
                        skill_label_data[j].push(this.skillTable[i].title)

                    }
                }
            }

            // let chart_input_button = document.getElementById('chart-input-button')
            //
            // if (this.user.is_student)
            //     chart_input_button.style.visibility = "hidden"
            // console.log(skill_label_data)
            let chart_ids = ['chart-1', 'chart-2']
            // let chart_input_ids = ['chart-1-inputs', 'chart-2-inputs']

            for(let i = 0; i < n_types; ++i){


                const ctx = document.getElementById(chart_ids[i]).getContext('2d');

                const chart_data = {
                    labels: skill_label_data[i]
                }

                if (this.user.is_student){
                chart_data.datasets = [
                    {
                    label: 'My Skills',
                    data: chart_freq_data[i],
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                    },
                    {
                    label: 'Goal',
                    data: goal_freq_data[i],
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                    },
                    ]
                }

            else if (this.user.is_staff){
                chart_data.datasets = [{
                    label: 'Goal',
                    data: chart_freq_data[i],
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
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
                this.radarcharts.push(new Chart(ctx, config))
            }

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
            // console.log(this.user)
            this.user['is_staff'] = Object.values(this.user.groups).includes('staff')
            this.user['is_student'] = Object.values(this.user.groups).includes('student')

            this.prepareChartData()


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
        // user:{},
        // profile:{}, //Get Curriculum id
        // curriculums:[],
        // skillgroups:[],
        // skillTable:[],
        // events:[],

        axios.get(variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;

                });

        //Return a list of one element.
        axios.get(variables.API_URL+"student")
                .then((response)=>{
                this.profile=response.data[0];
                });

        //Consider returning only the curriculum enrolled by the student.
        axios.get(variables.API_URL+"curriculum")
                .then((response)=>{
                this.curriculums=response.data;
                });

        axios.get(variables.API_URL+"skillgroup")
                .then((response)=>{
                this.skillgroups=response.data;
                });

        axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
            });

        axios.get(variables.API_URL+"eventAttended/list")
            .then((response)=>{
                this.events=response.data;
            });


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
    }
})

app.mount('#app')




