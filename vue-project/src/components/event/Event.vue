<script>
import { Multiselect } from 'vue-multiselect'
import { VueGoodTable } from 'vue-good-table';
import axios from 'axios'

import flatpickr from 'flatpickr'
import 'flatpickr/dist/flatpickr.min.css'

import * as bootstrap from 'bootstrap' //where is bootstrap-icons??

import 'vue-datetime/dist/vue-datetime.min.css'

export default {
    components: {

        VueGoodTable,
        Multiselect,
        
    },

    data() {
        return {

            events: [],
            user: {},

            modalTitle: "",
            addingNewEvent: false,
            showApproved: true,
            modalReadonly: false,

            event: {},
            copiedEvent : {},

            skillTable: [],
            staffTable: [],
            checkboxes: [],
            checkboxFields: ['approved', 'used_for_calculation', 'arranged_inside'],

            formKey:1,
            testMode:false,

            formConstraints : {
                attachment_file : {
                    max_file_size : {
                        'size' : 2000000,
                        'validation_message' : this.attachment_file_max_file_size_validation_message_function,
                        'validation_rule' : this.attachment_file_max_file_size_validation_function
                    }
                },   
            },

            vgtColumns : [
                {
                    label: 'Event ID',
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
                    label: 'Start',
                    field: 'start_datetime',
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-MM-dd\'T\'HH:mm",
                    dateOutputFormat: "dd-MM-yyyy HH:mm",
                    thClass: 'text-center',
                    tdClass: 'text-center',
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Start",
                        filterFn: this.datetimeRangeFilter,
                    }

                },
                {
                    label: 'Start',
                    field: 'end_datetime',
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-MM-dd\'T\'HH:mm",
                    dateOutputFormat: "dd-MM-yyyy HH:mm",
                    thClass: 'text-center',
                    tdClass: 'text-center',
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Start",
                        filterFn: this.datetimeRangeFilter,
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
    methods: {
        getEmptyEvent() {
            return {
                id: 0,
                title: "",
                start_datetime: (new Date()).toLocaleString(),
                end_datetime: (new Date()).toLocaleString(),
                info: "",

                created_by: "",
                approved: false,
                approved_by: "",
                used_for_calculation: false,
                arranged_inside: false,
                attachment_link: "",
                attachment_file: "",

                //Additional data.
                skills: [],
                staffs: [],
            }
        },

        refreshData() {
            axios.get(this.$API_URL + "event")
                .then((response) => {
                    this.events = response.data;
                });

            // this.event = this.getEmptyEvent()
            // this.checkboxes = []
        },
        addClick(){

            this.modalTitle="Add Event"
            this.addingNewEvent= true 

            this.event = this.getEmptyEvent()
            this.checkboxes=[]

        },

        viewClick(event){
            this.modalTitle="Event (read only mode)";
            this.addingNewEvent = false
            this.modalReadonly = true

            this.event = JSON.parse(JSON.stringify(event))
            this.copiedEvent = JSON.parse(JSON.stringify(event))

            this.checkboxes = []
            for(let i=0; i<this.checkboxFields.length; ++i){
                if (this.event[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i])
            }
        },

        editClick(event) {

            this.modalTitle = "Edit Event";
            this.addingNewEvent = false
            this.modalReadonly = false

            this.event = JSON.parse(JSON.stringify(event))
            this.copiedEvent = JSON.parse(JSON.stringify(event))

            this.checkboxes = []
            for (let i = 0; i < this.checkboxFields.length; ++i) {
                if (this.event[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i])
            }

        },

        createClick() {

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: this.$API_URL + "event",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            }).catch((errors) => {
                console.log(errors)
            })
        },

        updateClick() {

            //Form validation

            for (let i = 0; i < this.checkboxFields.length; ++i)
                this.event[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outDict.append(key.toString(), value)
            }

            outDict.set('attachment_file', this.cleanAttachmentFile(this.event.attachment_file))
            outDict.set('skills', JSON.stringify(this.cleanManyToManyFields(this.event.skills)))
            outDict.set('staffs', JSON.stringify(this.cleanManyToManyFields(this.event.staffs)))

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: this.$API_URL + "event/" + this.event.id,
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outDict,
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response) => {
                this.reassignUpdatedElementIntoList(this.events, response.data)
                this.event = JSON.parse(JSON.stringify(response.data))
                this.copiedEvent = JSON.parse(JSON.stringify(response.data))
                alert(JSON.stringify(response.data));

            }).catch((errors) => {
                console.log(errors)
            })

        },

        deleteClick(event_id) {

            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: this.$API_URL + "event/" + event_id,
                xstfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {
                    'X-CSRFToken': 'csrftoken',
                }
            }).
                then((response) => {
                    this.refreshData();
                    alert(response.data);
                })

        },
        cleanManyToManyFields(list){
            //Remove empty or redundant inputs.
            // console.log(list)
            let nonEmpty = []
            let ids = []
            for (let i=0;i<list.length; ++i) {
                let id = list[i]['id']

                if ( id !== '' && !ids.includes(id)){
                    ids.push(list[i].id);
                    nonEmpty.push({'id' :list[i].id} )
                }
            }

            return nonEmpty
        },
        cleanAttachmentFile(attachment_file_field){
            // Idea : If there is a file, send it.

            let file_field = attachment_file_field

            if (! Object.is(file_field, null)){
                if (typeof file_field !== 'string')
                    if ( ! Object.is(file_field.files, null))
                        if (file_field.files.length !== 0)
                            return file_field.files[0].file
            }
            
            return file_field
        },

        reassignUpdatedElementIntoList(list, element){
            for (let i = 0; i < list.length; ++i){
                if (list[i].id === element.id){
                    this.$set(list, i, element)
                    break;
                }
            }
        },

        openNewWindow(url) {
            window.open(url);
        },

        _skill_custome_label({id, title}){
            if (id === '' || Object.is(id,  null)){
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

        _staff_custom_label({id, university_id, firstname, lastname}){

            if (id === '' || Object.is(id,  null)){
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
        attachment_file_max_file_size_validation_function(){
            //Idea : If the file exists, the size must be valid.
            
            let maxFileSize = this.formConstraints.attachment_file.max_file_size.size
            console.log(this.formConstraints)
            console.log(this.event)

            let file_field = this.event.attachment_file
            
            
            if (typeof file_field === 'string'){
                return true
            }else if ( Object.is(file_field, null) ){
                return true
            }else if (file_field.files.length === 0){
                return true
            }else{
                return file_field.files[0].file.size < maxFileSize
            }
        },

        attachment_file_max_file_size_validation_message_function(){
            return 'The file size must not exceed ' + this.formConstraints.attachment_file.max_file_size.size + ' bytes.'
        },

        toggleColumn( index, event ){
            // Set hidden to inverse of what it currently is
            this.$set( this.vgtColumns[ index ], 'hidden', ! this.vgtColumns[ index ].hidden );
        },

        datetimeRangeFilter(data, filterString) {

            let dateRange = filterString.split("to");
            let startDate = Date.parse(dateRange[0]);
            let endDate = Date.parse(dateRange[1]);
            return (Date.parse(data) >= startDate && Date.parse(data) <= endDate);

        },
    
    },

    created: async function () {
        this.event = this.getEmptyEvent()

        if (this.testMode)
            return;

        await axios.get(this.$API_URL + "user")
            .then((response) => {
                this.user = response.data;
                console.log(this.user)
            });

        axios.get(this.$API_URL + "event")
            .then((response) => {
                this.events = response.data;
                console.log(this.events)
            });

        axios.get(this.$API_URL + "staff")
            .then((response) => {
                this.staffTable = response.data;
                console.log(this.staffTable)
            });

        axios.get(this.$API_URL + "skillTable")
            .then((response) => {
                this.skillTable = response.data;
                console.log(this.skillTable)
            });

        },

    mounted: function () {
        
        let inputs = [
          'input[placeholder="Filter Start"]',
          // 'input[placeholder="Filter Start Date"]'
          // 'input[placeholder="Filter Need By Date"]'
        ];

        inputs.forEach(function(input) {
            flatpickr(input, {
            dateFormat: "d-m-Y",
            mode: "range",
            allowInput: true,
            enableTime:true,
            });
        });

        document.getElementById('edit-info-modal').addEventListener('hidden.bs.modal', (event)=> {
            this.veeErrors.clear()
            this.formKey += 1
            
        })
    }
}
</script>


<template>
    <div>

        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
            Add Event
        </button>

        <vue-good-table

            ref="vgt"
            :columns="vgtColumns"
            :rows="events"
            :select-options="{
                enabled: true,
                selectOnCheckboxOnly: true, // only select when checkbox is clicked instead of the row
            }"
            :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 10,
                setCurrentPage: 1,
            }"

        >

            <div slot="table-actions">
                <div class="dropdown">

                      <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        columns
                      </button>
                      <!-- <input :checked="!column.hidden" type="checkbox" disabled/> -->
                      
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="index" href="#"> 
                                <span href="#" class="small" tabIndex="-1" @click.prevent="toggleColumn(index, $event)" >
                                    <formulate-input type="checkbox" v-if="!column.hidden" disabled="true" checked="true"></formulate-input>
                                    {{ column.label }}
                                </span>
                            </a>
                      </div>

                </div>

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
                        :id="'edit-button-' + props.row.id"
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
                  {{ props.formattedRow[props.column.field] }}
                </span>
          </template>

        </vue-good-table>
        




        <div class="modal fade" id="edit-info-modal" tabindex="-1" aria-labelledby="edit-info-modal-label"
            aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered">

                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="edit-info-modal-label">{{ modalTitle }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">


                                <button v-if="!addingNewEvent && user.is_staff" type="button"
                                    class="btn btn-primary m-2 fload-end"
                                    v-on:click="openNewWindow('/event-attendance/' + event.id)">
                                    Show Attendances
                                </button>
                                
                                <FormulateForm name="formulate-form-1" ref="formulate-form-1" #default="{ hasErrors }" :key="formKey">
                                    <formulate-input ref="formulate-input-title" type="text" v-model="event.title" label="Title" validation="required|max:100" :readonly="modalReadonly"></formulate-input>
                                    <FormulateInput ref="formulate-input-start_datetime" type="vue-datetime"  datetype="datetime" v-model="event.start_datetime" label="Start" validation="required"  :disabled="modalReadonly"></FormulateInput>
                                    <FormulateInput ref="formulate-input-end_datetime" type="vue-datetime"  datetype="datetime" v-model="event.end_datetime" label="End" validation="required"  :disabled="modalReadonly"></FormulateInput>
                                    <formulate-input ref="formulate-input-info" label="Info" type="textarea" v-model="event.info" validation="max:200,length" :readonly="modalReadonly" validation-name="info"></formulate-input>
                                    
                                    <h3>Skills</h3>
                                    <multiselect v-model="event.skills" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="skillTable" :custom-label="_skill_custome_label" track-by="id" placeholder="Select..." :disabled="modalReadonly">
                                    </multiselect>

                                    <h3>Staffs</h3>
                                    <multiselect v-model="event.staffs" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="staffTable" :custom-label="_staff_custom_label" track-by="id" placeholder="Select..." :disabled="modalReadonly"></multiselect>
                                    
                                    <p></p>
                                    <FormulateInput  ref="formulate-input-approved" v-model="checkboxes" :options="{approved : 'approved'}" type="checkbox" :disabled="modalReadonly || !user.is_staff"></FormulateInput>
                                    <FormulateInput  ref="formulate-input-used_for_calculation" v-model="checkboxes" :options="{used_for_calculation : 'Use for calculation'}" type="checkbox" :disabled="modalReadonly || !user.is_staff"></FormulateInput>
                                    <FormulateInput  ref="formulate-input-attachment_link" type="url" v-model="event.attachment_link"                                            
                                            label="Attachment link" placeholder="URL" validation="" :disabled="modalReadonly" >
                                    </FormulateInput>                                           
                                        
                                    <FormulateInput
                                        type="file" ref="formulate-input-attachment_file" name="formulate-input-attachment_file"
                                        
                                        v-model="event.attachment_file" label="Attachment file"                                  
    
                                        

                                        error-behavior="live" validation-event="input" validation="" upload-behavior="delayed" :disabled="modalReadonly" >
                                    </FormulateInput>
                            

                                        
                                </FormulateForm>
                            
                                <hr>

                            </div>

                        </div>

                        <div class="modal-footer">
                            <button id="createButton" type="button" @click="createClick()" v-if="addingNewEvent"
                                class="btn btn-primary">
                                Create
                            </button>

                            <button id="updateButton" type="button" @click="updateClick()" v-else class="btn btn-primary">
                                Update
                            </button>
                        </div>

                    </div>

                </div>
            </div>
        </div>


    </div>
</template>