
let chartComponent = {
    template: '#chart-template',

    data(){
        return{
            //API Zone
            user:{},
            profile:{}, //Get Curriculum id from enroll.
            curriculums:[],
            skillgroups:[],
            skillTable:[],
            events:[],



            // JS editing zone
            modalTitle:"Edit goal points",
            n_groups:0,
            max_n_groups:5,

            reindexedSkillTable:{},
            skillFreq:[],
            skillLabels:[],

            radarCharts:[],
            chartActive:false,
            // checkboxes: [],

        }
    },

    methods:{
        refreshData(){

        },

        getEmptyArrayOfArrays(arrayLength){
            let arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i ){
                arr[i] = []
            }

            return arr
        },

        getEmptyArrayOfDicts(arrayLength){
            let arr = new Array(arrayLength)
            for (let i = 0; i < arrayLength; ++i ){
                arr[i] = {}
            }

            return arr
        },

        reloadCharts(){
             //Prepare chartFreqData for each chart.
            let curriculum_id = this.profile.enroll
            let curriculum = ''
            // console.log('curriculumxxxxx')
            for (let i = 0; i < this.curriculums.length; ++i){
                if (this.curriculums[i].id === curriculum_id){
                    curriculum = this.curriculums[i]
                    // console.log(this.curriculums[i])
                    break;
                }

            }

            let skillgroups_for_charts = []
            // console.log('curriculum')
            // console.log(curriculum)

            for(let i = 0; i < this.skillgroups.length; ++i){
                for(let j = 0; j < curriculum.skillgroups.length; ++j)
                    if (this.skillgroups[i].id === curriculum.skillgroups[j].id){
                        skillgroups_for_charts.push(JSON.parse(JSON.stringify(this.skillgroups[i])))
                    }
            }

            // let skills_for_charts = this.getEmptyArrayOfDicts(skillgroups_for_charts.length)
            // for(let i = 0; i < skills_for_charts.length; ++i){
            //
            //     for(let j = 0; j < skillgroups_for_charts.skills.length; ++j){
            //         skills_for_charts[i][ skillgroups_for_charts.skills[j].skill_id_fk ] = skillgroups_for_charts.skills[j]
            //     }
            // }

            this.n_groups = skillgroups_for_charts.length
            // this.chartActive = true

            let chart_freq_data = this.getEmptyArrayOfArrays(this.n_groups)
            let goal_freq_data = this.getEmptyArrayOfArrays(this.n_groups)
            let skill_label_data = this.getEmptyArrayOfArrays(this.n_groups)



            // console.log(skillgroups_for_charts)
            // console.log(skillgroups_for_charts.skills)
            for(let i = 0; i < skillgroups_for_charts.length ; ++i ){
                for (let j = 0; j < skillgroups_for_charts[i].skills.length; ++j){

                    let temp_skill_id = skillgroups_for_charts[i].skills[j].skill_id_fk
                    // console.log(temp_skill_id)
                    // console.log(this.skillTable)
                    chart_freq_data[i].push( this.skillFreq[ temp_skill_id ])
                    goal_freq_data[i].push( skillgroups_for_charts[i].skills[j].goal_point )
                    skill_label_data[i].push(this.reindexedSkillTable[ temp_skill_id ].title)
                }
            }


            // for (let i = 0; i < this.skillTable.length; ++i){
            //     for (let j = 0; j < n_groups; ++j){
            //         chart_freq_data[j].push(this.skillFreq[i])
            //         goal_freq_data[j].push(skillgroups_for_charts.skills.skill_id_fk)
            //     }
            // }
            //
            // for (let i = 0; i < this.skillTable.length; ++i){
            //     for (let j = 0; j < n_groups; ++j){
            //         if (this.skillTable[i].type === (j+1)){
            //             chart_freq_data[j].push(this.skillFreq[i])
            //             goal_freq_data[j].push(this.skillTable[i].goal_point)
            //             skill_label_data[j].push(this.skillTable[i].title)
            //
            //         }
            //     }
            // }

            let chart_ids = []
            for (let i = 0; i < this.n_groups; ++i){
                chart_ids.push('chart-' + (i + 1))
            }

            // console.log(chart_ids)
            this.radarcharts = []
            for(let i = 0; i < this.n_groups; ++i){

                // console.log(document.getElementById(chart_ids[i]))
                const ctx = document.getElementById(chart_ids[i]).getContext('2d');

                const chart_data = {
                    labels: skill_label_data[i]
                }


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


            let skillFreq = {}
            for (let i=0; i<this.skillTable.length; ++i){
                skillFreq[this.skillTable[i].id] = 0
            }

            for (let i=0; i < this.events.length; ++i){
                for (let j=0; j < this.events[i].skills.length; ++j){
                    skillFreq[this.events[i].skills[j].id] += 1
                }
            }

            let reindexedSkillTable = {}
            for (let i=0; i< this.skillTable.length; ++i){
                reindexedSkillTable[this.skillTable[i].id] = this.skillTable[i]
            }
            this.reindexedSkillTable = reindexedSkillTable


            this.skillFreq = skillFreq


            //Initialize skillLabels
            // let skillLabels = []
            // this.skillTable.forEach(function(e) {
            //         skillLabels.push(e.title)
            //     }
            // )
            // this.skillLabels = skillLabels

        },

        prepareData(){
            // console.log(this.user)
            // this.user['is_staff'] = Object.values(this.user.groups).includes('staff')
            // this.user['is_student'] = Object.values(this.user.groups).includes('student')

            this.prepareChartData()


        },
    },

    created: async function(){

    },

    mounted: async function(){

        await axios.get(variables.API_URL+"user")
                .then((response)=>{
                this.user=response.data;
                });

        //Return a list of one element.
        await axios.get(variables.API_URL+"student")
                .then((response)=>{
                this.profile=response.data[0];
                console.log(this.profile)
                });

        //Consider returning only the curriculum enrolled by the student.
        await axios.get(variables.API_URL+"curriculum")
                .then((response)=>{
                this.curriculums=response.data;
                console.log(this.curriculums)
                });

        await axios.get(variables.API_URL+"skillgroup")
                .then((response)=>{
                this.skillgroups=response.data;
                console.log(this.skillgroups)
                });

        await axios.get(variables.API_URL+"skillTable")
            .then((response)=>{
                this.skillTable=response.data;
                console.log(this.skillTable)
            });

        await axios.get(variables.API_URL+"event-attended/list")
            .then((response)=>{
                this.events=response.data;
                console.log(this.events)
            });

        this.prepareData()
        this.reloadCharts()
    }
}
const app = Vue.createApp({
    components: {
        'chart-html' : chartComponent,
        // 'goal-chart-html' : goalChartComponent,
    }
})

app.mount('#app')




