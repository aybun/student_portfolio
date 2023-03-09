<script>


// import { VueGoodTable  } from 'vue-good-table';
import { Multiselect } from 'vue-multiselect'
import { VueGoodTable } from  'vue-good-table';
import axios from 'axios'
import flatpickr from 'flatpickr'
// import VueFormulate from '@braid/vue-formulate'

export default {

components:{
    
    Multiselect: Multiselect,
    VueGoodTable,
    // VueFormulate, 

},
// mixins: [VueFormulate.FormulateMixin],
// plugins: [VueFormulate.default],

data()  {
    return {
        modalTitle:"",
        addingNewAward:false,
        formKey:1,
        showApproved:true,
        // showUnapproved:false,
        // showOptions:true,

        staffTable:[],
        studentTable:[], //Define user Api.


        user:{},

        award:{},
        copiedAward:{},
        awards:[],


        // formReceiversIsValid: true,

        checkboxes:[],
        checkboxFields : ['approved', 'used_for_calculation'],
        formulateInputFieldRefs: [
            'formulate-input-title', 'formulate-input-rank',
            'formulate-input-received_date', 'formulate-input-info',
            'formulate-input-approved', 'formulate-input-used_for_calculation',
            "formulate-input-attachment_link", 'formulate-input-attachment_file'],

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
        axios.get(this.$API_URL + "award").
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
            url: this.$API_URL+"award",
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
        this.copiedAward = JSON.parse(JSON.stringify(award))

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
        this.copiedAward = JSON.parse(JSON.stringify(award))

        this.checkboxes = []
        for(let i=0; i<this.checkboxFields.length; ++i){
            if (this.award[this.checkboxFields[i]])
                this.checkboxes.push(this.checkboxFields[i])
        }

    },
    async updateClick(){

        let formIsValid =  false;
        await this.validateForm().then((result) => {
             formIsValid = result
        })

        if (!formIsValid)
            return;

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
        // typeof myVar === 'string' || myVar instanceof String

        if (! Object.is(this.award.attachment_file, null)){
            if (typeof this.award.attachment_file !== 'string')
                if ( ! Object.is(this.award.attachment_file.files, null))
                    if (this.award.attachment_file.files.length !== 0)
                        outDict.set('attachment_file', this.award.attachment_file.files[0].file)
        }

        outDict.set('skills', JSON.stringify(this.award.skills))
        outDict.set('receivers', JSON.stringify(this.award.receivers))
        outDict.set('supervisors', JSON.stringify(this.award.supervisors))

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios({
            method: 'put',
            url: this.$API_URL+"award/" + this.award.id,
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{

            this.reAssignUpdatedElementIntoList(response.data) //With reactivity.
            this.award = JSON.parse(JSON.stringify(response.data))
            this.copiedAward = JSON.parse(JSON.stringify(response.data))

            alert(JSON.stringify(response.data));
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
            url: this.$API_URL+"award/"+ award_id,
            xsrfCookieName: 'csrftoken',
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
            url: this.$API_URL+"award/multi-delete",
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            data: outDict,
            headers : {
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            // this.refreshData();

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
    },
    reAssignUpdatedElementIntoList(newAward){

        for (let i = 0; i < this.awards.length; ++i){
            if (this.awards[i].id === newAward.id){
                this.$set(this.awards, i, newAward)
                break;
            }
        }
    }
    ,
    validateAttachmentFileLessThan2MB(maxFileSize){

        if (typeof this.award.attachment_file == 'string'){
            return true
        }else if (Object.is(this.award.attachment_file, null)){
            return true
        }else if (this.award.attachment_file.files.length === 0){
            return true
        }else{
            return this.award.attachment_file.files[0].file.size < maxFileSize
        }

    },

    async validateForm(){
        //return boolean
        // vur-formulate

        // const vue_formulate_promises = [];
        //
        // this.formulateInputFieldRefs.forEach((e) => {
        //     vue_formulate_promises.push(this.$refs[e].performValidation())
        // })
        // await Promise.all(vue_formulate_promises)

        //Perform validation on the form.
        await this.$formulate.submit('formulate-form-1');

        let vue_formulate_valid = this.$refs['formulate-form-1'].isValid;
        // console.log(vue_formulate_valid)

        //vee-validate
        await this.$validator.validate().then((result) => {
            return result
        });


        let vee_validate_valid = (!this.veeErrors.has('multiselect-receivers'))

        return vue_formulate_valid && vee_validate_valid
    },

},

created: async function(){
    
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    await axios({
            method: 'get',
            url: this.$API_URL+"user",
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFToken',
            headers : {
                'X-CSRFToken': 'csrftoken',
            }
        }).then((response)=>{
            this.user=response.data;
        })
    
    // await axios.get(this.$API_URL+"user")
    //     .then((response)=>{
    //         this.user=response.data;
    //     })

    axios.get(this.$API_URL + "award")
        .then((response)=>{
            this.awards=response.data;
        })

    axios.get(this.$API_URL + "student")
        .then((response)=>{
            this.studentTable=response.data;
        })


    axios.get(this.$API_URL+"staff")
    .then((response)=>{
        this.staffTable=response.data;
        // console.log(this.staffTable)
    });

    axios.get(this.$API_URL+"skillTable")
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


mounted:function(){
    console.log('cookies', document.cookie)
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
        // console.log(this.$refs['formulate-input-attachment_file'])
        // this.$refs['formulate-input-attachment_file'];
        // this.award.attachment_file = ''
        this.veeErrors.clear()
        // console.log(this.$formulate)
        // this.$formulate.reset('formulate-input-attachment_file', '')
        // this.award = this.getEmptyAward()
        this.formKey += 1
        // this.$refs['formulate-form-1'].isValid
        // console.log(this.$refs['formulate-form-1'])


    })
}

}
</script>

<template>
  <div>
    <button type="button"
            class="btn btn-primary m-2 fload-end"
            data-bs-toggle="modal"
            data-bs-target="#edit-info-modal"
            @click="addClick()"
    >
         Create Award
    </button>

    <button type="button" class="btn btn-primary m-2 fload-end" v-on:click="showApproved = true">
         show approved
     </button>
    <button type="button" class="btn btn-primary m-2 fload-end" v-on:click="showApproved = false">
         show unapproved
     </button>

    <vue-good-table

        ref="vgt"
        :columns="vgtColumns"
        :rows="awards"
        :select-options="{enabled: true,
            selectOnCheckboxOnly: true, // only select when checkbox is clicked instead of the row
        }"
        :search-options="{ enabled: true }"
        :pagination-options="{
                            enabled: true,
                            mode: 'records',
                            perPage: 10,
                            setCurrentPage: 1,
                        }"
        @on-selected-rows-change="selectionChanged"

    >


        <div slot="selected-row-actions">
            <button @click="rowActionDelete">delete</button>
        </div>

        <div slot="table-actions">
            <div class="dropdown">

                  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    columns
                  </button>

                  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="index" href="#">
                            <a href="#" class="small" tabIndex="-1" @click.prevent="toggleColumn( index, $event )" ><input :checked="!column.hidden" type="checkbox"/>&nbsp;{% verbatim block %}{{column.label}}{% endverbatim block %}</a>
                        </a>
                  </div>

            </div>

<!--            <multiselect v-model="visibleColumns" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="skillTable" track-by="id" placeholder="Select..." :disabled="modalReadonly">-->

<!--            </multiselect>-->

        </div>

        <template slot="table-row" slot-scope="props">
            <span v-if="props.column.field == 'action'">

                <button v-if="user.is_staff || user.is_student" type="button"
                    class="btn btn-light mr-1"
                    data-bs-toggle="modal"
                    data-bs-target="#edit-info-modal"
                    @click="viewClick(props.row);">
                        <i class="bi bi-eye"></i>
                </button>

                <button v-if="user.is_staff || !props.row.approved && props.row.created_by === user.id && user.is_student" type="button"
                    class="btn btn-light mr-1"
                    data-bs-toggle="modal"
                    data-bs-target="#edit-info-modal"
                    @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                </button>

                <button v-if="user.is_staff || !props.row.approved && props.row.created_by === user.id && user.is_student" type="button" @click="deleteClick(props.row.id)"
                    class="btn btn-light mr-1">
                    <i class="bi bi-trash"></i>
                </button>
            </span>

            <span v-else>
              {% verbatim block %}{{props.formattedRow[props.column.field]}}{% endverbatim block %}
            </span>
      </template>
    </vue-good-table>

<!--    <div class="modal fade" id="edit-info-modal" tabindex="-1"-->
    <div class="modal fade" id="edit-info-modal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false"
         aria-labelledby="ModalLabel" aria-hidden="true">

        <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                    <h5 class="modal-title" id="ModalLabel">{% verbatim block %}{{modalTitle}}{% endverbatim block %}</h5>

                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <div class="modal-body">

                <div class="d-flex flex-row bd-highlight mb-3">

                    <div class="p-1 w-50 bd-highlight">
                        <FormulateForm name="formulate-form-1" ref="formulate-form-1" #default="{ hasErrors }">

                        <formulate-input ref="formulate-input-title" type="text" v-model="award.title" label="Title" validation="required" :readonly="modalReadonly"></formulate-input>

                        <formulate-input ref="formulate-input-rank" type="number" v-model="award.rank"  label="Rank" validation="required|number|min:0|max:5" :readonly="modalReadonly">

                        </formulate-input>


                        <formulate-input ref="formulate-input-received_date" type="date" v-model="award.received_date"  label="Received Date" validation="required" :readonly="modalReadonly"></formulate-input>

                        <formulate-input ref="formulate-input-info" label="Info" type="textarea" v-model="award.info" validation="max:200,length" :readonly="modalReadonly" validation-name="info"></formulate-input>


                        <div v-if="!addingNewAward" class="skill">
                            <h3>Skills</h3>

                            <multiselect v-model="award.skills" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="skillTable" :custom-label="skillCustomLabel" track-by="id" placeholder="Select..." :disabled="modalReadonly">

                            </multiselect>

                        </div>

                        <div v-if="user.is_staff && !addingNewAward" class="receiver">
                            <h3>Receivers</h3>
                            <div>

                                    <multiselect  ref="multiselect-receivers" name="multiselect-receivers" v-model="award.receivers"
                                                v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="receivers"

                                                  :hide-selected="true"  :close-on-select="false" :multiple="true" :options="studentTable" :custom-label="receiverCustomLabel" track-by="id" placeholder="Select..." :disabled="modalReadonly">

                                    </multiselect>
                                <span v-show="veeErrors.has('multiselect-receivers')" style="color:red;" >{% verbatim block %}{{ veeErrors.first('multiselect-receivers') }}{% endverbatim block %}</span>
                            </div>
                        </div>

                        <div v-if="!addingNewAward" class="staff">
                            <h3>Supervisors</h3>
                            <multiselect v-model="award.supervisors" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="staffTable" :custom-label="supervisorCustomLabel" track-by="id" placeholder="Select..." :disabled="modalReadonly"></multiselect>


                        </div>
<!--                            Still working on this.-->
                        <div v-if="!addingNewAward" class="mb-3">

                            <FormulateInput  ref="formulate-input-approved" v-model="checkboxes" :options="{approved : 'approved'}" type="checkbox" :disabled="modalReadonly || !user.is_staff"></FormulateInput>
                            <FormulateInput  ref="formulate-input-used_for_calculation" v-model="checkboxes" :options="{used_for_calculation : 'Use for calculation'}" type="checkbox" :disabled="modalReadonly || !user.is_staff"></FormulateInput>
                        </div>

                        <div v-if="!addingNewAward" class="mb-3">

                            <FormulateInput
                                  ref="formulate-input-attachment_link"
                                  type="url"
                                  v-model="award.attachment_link"
                                  label="Attachment link"
                                  placeholder="Copy and paste url here"
                                  help="copy and paste url"
                                  validation=""
                            ></FormulateInput>
                        </div>

                        <p></p>

                        <div v-if="!addingNewAward" class="mb-3">

                            <FormulateInput
                              :key="formKey"
                              type="file"

                              ref="formulate-input-attachment_file"
                              name="formulate-input-attachment_file"
                              v-model="award.attachment_file"

                              label="Attachment file"
                              help="The file size must not exceed 2MB."

                              :validation-rules="{lessThan2MB : () => {
                                    return validateAttachmentFileLessThan2MB(2000000)
                              }}"

                              :validation-messages="{
                                  lessThan2MB : 'The file size must not exceed 2MB.'
                               }"

                              error-behavior="live"
                              validation-event="input"
                              validation="lessThan2MB"

                              upload-behavior="delayed"

                              :disabled="modalReadonly"

                            ></FormulateInput>
<!--                            File Button-->
                            <button v-if="copiedAward.attachment_file != '' &&  !Object.is(copiedAward.attachment_file, null)" type="button" class="btn btn-primary" @click="this.window.open(award.attachment_file)"> File URL </button>
                            <button v-if="copiedAward.attachment_file != '' && !Object.is(copiedAward.attachment_file, null)" type="button" class="btn btn-outline-danger" @click="formKey += 1; copiedAward.attachment_file=''; award.attachment_file=''" :disabled="modalReadonly"> Remove File </button>

                        </div>

                        <!--                        <End of inputs>-->
                    <FormulateInput v-if="false"  type="submit" :disabled="hasErrors" @click="updateClick()">

                        Update

                    </FormulateInput>


                </FormulateForm>
                    </div>



                </div>

            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button id="createButton" type="button" @click="createClick()"
                    v-if="addingNewAward" class="btn btn-primary" >
                    Create
                </button>
<!--                type="button" class="btn btn-primary"-->
                <button type="button" class="btn btn-primary" v-if="!modalReadonly && !addingNewAward && (user.is_staff || user.is_student && (award.created_by == user.id))" id="updateButton"
                      @click="updateClick();">
                    Update
                </button>
            </div>

        </div>


        </div>

    </div>
</div>
</template>





<style scoped>

</style>
