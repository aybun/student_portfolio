let awardtComponent = {

    template : '#award-template',

    data(){
        return {
            modalTitle:"",
            addingNewAward:false,

            showApproved:true,
            // showUnapproved:false,
            // showOptions:true,

            staffTable:[],
            userTable:[], //Define user Api.


            user:{},

            award:{},
            awards:[],

            checkboxes:[],
            checkboxFields : ['approved', 'used_for_calculation'],
        }
    },

    methods:{
        getEmptyAward(){
            return {
                id:0,
                title:"",
                rank: 0,
                received_date: (new Date()).toISOString().split('T')[0],

                info:"",

                created_by:"",
                approved:false,
                approved_by:false,
                used_for_calculation:false,

                attachment_link:"",
                attachment_file:"",

                //many-to-many fields
                skills: [],
                receivers: [],
                supervisors: [],
            }
        },

        refreshData(){
            axios.get(variables.API_URL + "award").
             then((response)=>{
                this.awards=response.data;
            })
        },

        addClick(){

            this.modalTitle="Add Award"
            this.addingNewAward= true // Signal that we are adding new award.

            this.award = this.getEmptyAward()
            this.checkboxes=[]

        },
        createClick(){

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.award)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"award",
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
        editClick(award){
            this.modalTitle="Edit award";
            this.addingNewAward = false

            this.award = award

            this.checkboxes = []
            for(let i=0; i<this.checkboxFields.length; ++i){
                if (this.award[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i])
            }


        },
        updateClick(){
            this.award.skills = this.cleanManyToManyFields(this.award.skills);
            this.award.receivers = this.cleanManyToManyFields(this.award.receivers);
            this.award.supervisors = this.cleanManyToManyFields(this.award.supervisors);

            //CheckboxFields
            for (let i=0;i<this.checkboxFields.length; ++i)
                this.award[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.award)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('skills', JSON.stringify(this.award.skills))
            outDict.set('receivers', JSON.stringify(this.award.receivers))
            outDict.set('supervisors', JSON.stringify(this.award.supervisors))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"award/" + this.award.id,
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
        deleteClick(award_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"award/"+ award_id,
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

        addInputFieldClick(fieldName){
            this.award[fieldName].push({
                id:'',
            })
        },
        removeInputFieldClick(fieldName){
            this.award[fieldName].pop()
        },

        cleanManyToManyFields(list){
            //Remove empty or redundant inputs.
            nonEmpty = []
            ids = []
            for (let i=0;i<list.length; ++i) {
                id = list[i]['id']

                if ( id !== '' && !ids.includes(id)){
                    ids.push(list[i].id);
                    nonEmpty.push(list[i])
                }
            }
            return nonEmpty
        },

        onFileSelected(event){
            this.award.attachment_file = event.target.files[0]

        },
        prepareData(){
            this.award = this.getEmptyAward()

        }
    },

    created: async function(){
        await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            })

        axios.get(variables.API_URL + "award")
            .then((response)=>{
                this.awards=response.data;
            })

        axios.get(variables.API_URL + "student")
            .then((response)=>{
                this.userTable=response.data;
            })


        axios.get(variables.API_URL+"staff")
        .then((response)=>{
            this.staffTable=response.data;
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
        'award-html' : awardtComponent,
    }
})

app.mount('#app')