let awardtComponent = {

    template : '#award-template',
    components:{
        // 'v-select': VueSelect.VueSelect,
        Multiselect: window.VueMultiselect.default,
        'BootstrapTable': BootstrapTable,
        VueGoodTable : window['vue-good-table'].VueGoodTable,

    },
    // plugins: [VueFormulate.default],
    data(){
        return {
            modalTitle:"",
            addingNewAward:false,

            showApproved:true,
            // showUnapproved:false,
            // showOptions:true,

            staffTable:[],
            studentTable:[], //Define user Api.


            user:{},

            award:{},
            awards:[],


            formReceiversIsValid: true,


            checkboxes:[],
            checkboxFields : ['approved', 'used_for_calculation'],
            modalReadonly : false,

            // selectedRows: [],
            vgtColumns : [
                {
                    label: 'Award ID',
                    field: 'id',
                    tooltip: 'A simple tooltip',
                    thClass: 'text-center',
                    tdClass: 'text-center',
                },
                {
                    label: 'Title',
                    field: 'title',
                    thClass: 'text-center',

                    filterOptions: {
                        styleClass: 'class1', // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: 'Filter This Thing', // placeholder for filter input
                        filterValue: '', // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: 'Received date',
                    field: 'received_date',
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "yyyy-mm-dd",
                    thClass: 'text-center',
                    tdClass: 'text-center',
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Received",
                        filterFn: this.dateRangeFilter,
                    }

                },
                {
                    label: 'Approved',
                    field: 'approved',
                    thClass: 'text-center',
                    tdClass: 'text-center',
                    filterOptions: {
                        styleClass: 'class1', // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: 'All', // placeholder for filter input
                        filterValue: '', // initial populated value for this filter
                        filterDropdownItems: [true, false], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnApprovedFilterFn, //custom filter function that
                        trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: 'Action',
                    field: 'action',
                    thClass: 'text-center',
                    tdClass: 'text-center',
                },

            ],

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
            this.modalReadonly = false

            this.award = JSON.parse(JSON.stringify(award))

            this.checkboxes = []
            for(let i=0; i<this.checkboxFields.length; ++i){
                if (this.award[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i])
            }


        },
        viewClick(award){
            this.modalTitle="Award (read only mode)";
            this.addingNewAward = false
            this.modalReadonly = true

            this.award = JSON.parse(JSON.stringify(award))

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
            console.log('update')
            // console.log(this.$refs.formulateInputInfo)
            console.log(this.formReceiversIsValid)
            // console.log(this.$refs.formulateInputInfo.isValid)

            //CheckboxFields
            for (let i=0;i<this.checkboxFields.length; ++i)
                this.award[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

            // console.log('hello')
            // console.log(this.award)
            let outDict = new FormData();

            for (const [key, value] of Object.entries(this.award)) {
                outDict.append(key.toString(), value)
            }
            // typeof myVar === 'string' || myVar instanceof String
            if (typeof this.award.attachment_file != 'string'){
                outDict.set('attachment_file', this.award.attachment_file.files[0].file)
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
                    nonEmpty.push({'id' :list[i].id} )
                }
            }
            return nonEmpty
        },

        onFileSelected(event){
            this.award.attachment_file = event.target.files[0]

        },

        prepareData(){
            this.award = this.getEmptyAward()

        },

        //custom labels
        skillCustomLabel({id, title}){
            if (id === '' || id == null){

                return 'Select'
            }
            else if (title == null){
                for (let i = 0; i < this.skillTable.length; ++i){
                    if (this.skillTable[i].id === id){
                        let temp = this.skillTable[i]
                        return `${temp.id} ${temp.title}`
                    }
                }
            }

            return `${id} ${title}`
        },
        receiverCustomLabel({ id, university_id, firstname, lastname }){

            if (id === '' || id == null){

                return 'Select'
            }
            else if (university_id == null){
                for (let i = 0; i < this.studentTable.length; ++i){
                    if (this.studentTable[i].id === id){
                        let temp = this.studentTable[i]
                        return `${temp.university_id} ${temp.firstname} ${temp.lastname}`
                    }
                }
            }

            return `${university_id} ${firstname} ${lastname}`
        },

        supervisorCustomLabel({id, university_id, firstname, lastname}){

            if (id === '' || id == null){
                return 'Select'
            }
            else if (university_id == null){
                for (let i = 0; i < this.staffTable.length; ++i){
                    if (this.staffTable[i].id === id){
                        let temp = this.staffTable[i]
                        return `${temp.firstname} ${temp.lastname}`
                    }
                }
            }

            return `${firstname} ${lastname}`
        },

        clearAll(){
            console.log('clear all')
        },

        selectionChanged(params){
            // console.log('heloo')
            // let selectedRows = this.$refs['vgt'].selectedRows
            // console.log(selectedRows)
            // this.selectedRows = params.selectedRows
            // console.log(params)

        },

        rowActionDelete(){
            let selectedRows = this.$refs['vgt'].selectedRows
            console.log(selectedRows)

            let ids = []
            for(let i = 0; i < selectedRows.length; ++i){
                ids.push(selectedRows[i].id)
            }

            let outDict = new FormData();
            outDict.append('ids', JSON.stringify(ids))

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"award/multi-delete",
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers : {
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response)=>{
                this.refreshData();
                alert(response.data);
            })
        },

        dateRangeFilter(data, filterString) {

            let dateRange = filterString.split("to");
            let startDate = Date.parse(dateRange[0]);
            let endDate = Date.parse(dateRange[1]);
            return (Date.parse(data) >= startDate && Date.parse(data) <= endDate);

        },
        toggleColumn( index, event ){
            // Set hidden to inverse of what it currently is
            this.$set( this.vgtColumns[ index ], 'hidden', ! this.vgtColumns[ index ].hidden );
        },

        resetAwardFields(fieldname){

            if (fieldname === 'attachment_file'){
                this.$refs.attachment_file.reset();
            }
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
                this.studentTable=response.data;
            })


        axios.get(variables.API_URL+"staff")
        .then((response)=>{
            this.staffTable=response.data;
            // console.log(this.staffTable)
        });

        axios.get(variables.API_URL+"skillTable")
        .then((response)=>{
            this.skillTable=response.data;
        });

        this.prepareData()
    },

    computed : {
        // formReceiversIsInvalid () {
        //   return this.award.receivers.length === 0
        // }
    },

    watch:{
        award : {
            handler(newValue, oldValue) {
                // Note: `newValue` will be equal to `oldValue` here
                // on nested mutations as long as the object itself
                // hasn't been replaced.

                this.formReceiversIsValid = (newValue.receivers.length !== 0);
            },

            deep: true

        }
    },

    mounted:function(){
        // $('#table').bootstrapTable({
        //     // data: this.awards,
        //     // options : this.tableOptions,
        // });
        //https://stackoverflow.com/questions/18487056/select2-doesnt-work-when-embedded-in-a-bootstrap-modal/19574076#19574076
        // $.fn.modal.Constructor.prototype._enforceFocus = function() {};

        let inputs = [
              'input[placeholder="Filter Received"]',
              // 'input[placeholder="Filter Start Date"]'
              // 'input[placeholder="Filter Need By Date"]'
            ];

        inputs.forEach(function(input) {
            flatpickr(input, {
            dateFormat: "Y-m-d",
            mode: "range",
            allowInput: true
            });
        });
        // inputs.forEach(function(input) {
        //     $(input).daterangepicker({
        //         locale: {
        //             format: 'YYYY-MM-DD',
        //             separator: " to "
        //         }
        //     }
        //
        //     );
        // });

        document.getElementById('edit-info-modal').addEventListener('hidden.bs.modal', (event)=> {
            // document.getElementById('modal-form-attachment_file').reset()
            // if (event.target.getAttribute('data-dismiss') !== 'modal') {
            //     // If not, prevent the modal from closing
            //     event.preventDefault()
            // }

            // this.$refs['modal-form-attachment_file'].reset();

            // this.$refs['formulate-input-attachment_file'].reset();
            // this.award.attachment_file = ''
        })
    }

}

//Register vue-formulate
Vue.use(VueFormulate)

//Register vee-validate
// const veeValidateConfig = {
//   errorBagName: 'veeErrors', // change if property conflicts
// };

Vue.use(VeeValidate)


const app = new Vue({
    el: '#app',
    components:{
        'award-html' : awardtComponent,
        // 'validation-provider' : VeeValidate.ValidationProvider,
        // Multiselect: window.VueMultiselect.default,
        // 'v-select': VueSelect.VueSelect,
    },

    data () {
    return {
        options: [
          'foo',
          'bar',
          'baz'
        ]
    }
  }

})

// app.component('award-html', awardtComponent)
// app.component('vue-multiselect', window.VueMultiselect)
// app.component('v-select', VueSelect.VueSelect)
// app.mount('#app')