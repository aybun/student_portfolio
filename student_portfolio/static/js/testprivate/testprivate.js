let testprivateComponent = {

    template : '#testprivate-template',

    data(){
        return {
            modalTitle:"",
            addingNewItem:false,

            item : {},
            items : [],
        }
    },

    methods:{
        getEmptyItem(){
            return {
                id:0,

                private_file_1:"",
                private_file_2:"",
                created_by : 0,
            }
        },

        refreshData(){
            axios.get(variables.API_URL + "testprivate").
             then((response)=>{
                this.items=response.data;
            })
        },

        addClick(){

            this.modalTitle="Add Item"
            this.addingNewItem= true // Signal that we are adding new award.

            this.item = this.getEmptyItem()
            // this.checkboxes=[]

        },
        createClick(){

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.item)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"testprivate",
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
        editClick(item){
            this.modalTitle="Edit item";
            this.addingNewItem = false

            this.item = JSON.parse(JSON.stringify(item))

        },
        updateClick(){

            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.item)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"testprivate/" + this.item.id,
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

        deleteClick(item_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"testprivate/"+ item_id,
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



        onFileSelected_1(event){
            this.item.private_file_1 = event.target.files[0]
        },
        onFileSelected_2(event){
            this.item.private_file_2 = event.target.files[0]
        },

        prepareData(){
            this.item = this.getEmptyItem()

        }
    },

    created: async function(){
        await axios.get(variables.API_URL+"user")
            .then((response)=>{
                this.user=response.data;
            })

        axios.get(variables.API_URL + "testprivate")
            .then((response)=>{
                this.items=response.data;
            })

        axios.get(variables.API_URL + "student")
            .then((response)=>{
                this.studentTable=response.data;
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
        'testprivate-html' : testprivateComponent,
    }
})

app.mount('#app')