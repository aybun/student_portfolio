let eventComponent = {
    template: '#curriculum-template',

    data(){
        return {
            curriculum:{},
            curriculums:{},


            skillGroupTable:{},

            addingNewElement:false,
            modalTitle:"",

        }
    },

    methods: {
        refreshData(){
            axios.get(variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });
        }
    },

    created: function(){
        axios.get(variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });

        axios.get(variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillGroupTable=response.data;
            });


    },

    mounted:function(){

    },

}


const app = Vue.createApp({
    components: {'curriculum-html' : curriculumComponent},

})

app.mount('#app')