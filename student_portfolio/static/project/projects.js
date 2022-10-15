let projectComponent = {

    template : '#project-template',

    data(){
        return {
            modalTitle:"",
            addingNewProject:false,

            showApproved:true,
            // showUnapproved:false,
            // showOptions:true,

            staffs:[],
            user:{},

            project:{},
            projects:[],

            checkboxes:[],

        }
    },

    methods:{

        refreshData(){
            axios.get(variables.API_URL + "project").
             then((response)=>{
                this.projects=response.data;
            })
        },

        addClick(){
            console.log(this.projects)
            this.modalTitle="Add Project"
            this.addingNewProject= true // Signal that we are adding new project.

            this.project = this.getEmptyProject()
            this.checkboxes=[]

        },
        createClick(){

            this.project.skills = this.cleanSkills(this.project.skills);

            // if (this.project.attachment_file == null || typeof this.project.attachment_file === 'string' || this.project.attachment_file === '' )
            //     delete this.project.attachment_file

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.project)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skills', JSON.stringify(this.project.skills))
            // console.log(outDict.skills)

            alert(JSON.stringify(outDict, null, 2))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"project",
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
        editClick(project){
            this.modalTitle="Edit project";
            this.addingNewProject = false

            this.project = project
            this.checkboxes = []

            if (project.approved)
                this.checkboxes.push('approved')
            if (project.used_for_calculation)
                this.checkboxes.push('used_for_calculation')


        },
        updateClick(){
            //Note : Check if the project has already been approved. The frontend must prevent it from being unchecked.
            // let before_altered_project = this.getEmptyProject()

            this.project.skills = this.cleanSkills(this.project.skills);
            // before_altered_project.skills = this.project.skills

            // this.project.skills = JSON.stringify(this.project.skills)

            this.project.approved = this.checkboxes.includes('approved')
            this.project.used_for_calculation = this.checkboxes.includes('used_for_calculation')

            // if (this.project.attachment_file == null || typeof this.project.attachment_file === 'string' || this.project.attachment_file === '' )
            //     delete this.project.attachment_file

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.project)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skills', JSON.stringify(this.project.skills))
            // this.project.skills = before_altered_project.skills

            alert(JSON.stringify(outDict, null, 2))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"project/" + this.project.projectId,
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
        deleteClick(projectId){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"project/"+ projectId,
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
            this.project.skills.push({
                skillId: '',
            })
        },
        removeSkillClick(){
            this.project.skills.pop()
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


        getEmptyProject(){
            return {
                projectId:0,
                title:"",
                start_date: (new Date()).toISOString().split('T')[0],
                end_date: (new Date()).toISOString().split('T')[0],
                mainStaffId:"",
                info:"",

                skills:[],
                proposed_by:"",
                approved:false,
                approved_by:false,
                used_for_calculation:false,

                attachment_link:"",
                attachment_file:""
            }
        },
        onFileSelected(event){
            this.project.attachment_file = event.target.files[0]

        },
        prepareData(){
            this.project = this.getEmptyProject()
            // if (this.user.is_student)
            //     this.showOptions = false

        }
    },

    created: async function(){
         await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            })

         axios.get(variables.API_URL + "project").
             then((response)=>{
                this.projects=response.data;
            })

        axios.get(variables.API_URL+"staff")
        .then((response)=>{
            this.staffs=response.data;
        });

        axios.get(variables.API_URL+"skillTable")
        .then((response)=>{
            this.skillTable=response.data;
        });

        this.prepareData()
    },

    mounted:function(){

    }

}

const app = Vue.createApp({

    components:{
        'project-html' : projectComponent,
    }
})

app.mount('#app')