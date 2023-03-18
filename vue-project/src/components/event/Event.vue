<script>
import { Multiselect } from 'vue-multiselect'
import { VueGoodTable } from 'vue-good-table';
import axios from 'axios'

import flatpickr from 'flatpickr'
import 'flatpickr/dist/flatpickr.min.css'

import * as bootstrap from 'bootstrap' //where is bootstrap-icons??
import 'vue-datetime/dist/vue-datetime.min.css'

import { $vfm, VueFinalModal, ModalsContainer } from 'vue-final-modal'

// components
import EventAttendance from "/src/components/event/EventAttendance.vue";
import AttendanceModal from "/src/components/event/AttendanceModal.vue";

export default {
    components: {

        VueGoodTable,
        Multiselect,
        
        VueFinalModal,
        
        //Custom components
        AttendanceModal,
        EventAttendance,
    },

    data() {
        return {

            events: [],
            user: {},

            modalTitle: "",
            addingNewEvent: false,
            showApproved: true,
            modalReadonly: false,

            showEventAttendanceModal:false,

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

            formRenderSpec : {
                'staff' : {
                    'edit' : {
                        'mode' : 'exclude',
                        'fields' : []
                    },
                },

                'student' : {
                    'edit' : {
                        'mode' : 'exclude',
                        'fields' : ['used_for_calculation', 'approved']
                    },
                }

            },
            
            formRender : {},
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

        },
        addClick(){
            this.modalTitle="Add Event"
            this.addingNewEvent= true 
            this.modalReadonly = false

            this.assignDataToEventForm(this.getEmptyEvent())
        },

        viewClick(event){
            this.modalTitle="Event (read only mode)";
            this.addingNewEvent = false
            this.modalReadonly = true

            this.assignDataToEventForm(event)
        },

        editClick(event) {

            this.modalTitle = "Edit Event";
            this.addingNewEvent = false
            this.modalReadonly = false

            this.assignDataToEventForm(event)
        },
        assignDataToEventForm(event){
            let stringified = JSON.stringify(event)
            this.event = JSON.parse(stringified)
            this.copiedAward = JSON.parse(stringified)

            this.checkboxes = this.getListOfTrueCheckboxFields(this.event, this.checkboxFields)
        },
        
        getListOfTrueCheckboxFields(formdata, checkboxFields){

            let checkboxes = []
            for(let i=0; i < checkboxFields.length; ++i){
                if (formdata[checkboxFields[i]] === true)
                checkboxes.push(this.checkboxFields[i])
            }
            return checkboxes
        },

        assignBooleanValueToCheckboxFields(formdata, checkboxes, checkboxFields){
            for (let i=0; i < checkboxFields.length; ++i){
                let field_name = checkboxFields[i]
                formdata[field_name] = checkboxes.includes(field_name)
            }
        },

        async createClick() {
            let formIsValid =  false;
            await this.validateForm().then((result) => {
                formIsValid = result
            })

            if (typeof testMode !== 'undefined')
                this.eventFormHasbeenSubmitted = formIsValid;

            if (!formIsValid)
                return;
            //Packing values.
            this.assignBooleanValueToCheckboxFields(this.event, this.checkboxes, this.checkboxFields)
            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('attachment_file', this.cleanAttachmentFile(this.event.attachment_file))
            outDict.set('skills', JSON.stringify(this.cleanManyToManyFields(this.event.skills)))
            outDict.set('staffs', JSON.stringify(this.cleanManyToManyFields(this.event.staffs)))

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

        async updateClick() {

            //Form validation
            let formIsValid =  false;
            await this.validateForm().then((result) => {
                formIsValid = result
            })

            if (!formIsValid)
                return;

            this.assignBooleanValueToCheckboxFields(this.event, this.checkboxes, this.checkboxFields)
            let outForm = new FormData();
            for (const [key, value] of Object.entries(this.event)) {
                outForm.append(key.toString(), value)
            }
            outForm.set('attachment_file', this.cleanAttachmentFile(this.event.attachment_file))
            outForm.set('skills', JSON.stringify(this.cleanManyToManyFields(this.event.skills)))
            outForm.set('staffs', JSON.stringify(this.cleanManyToManyFields(this.event.staffs)))

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

                let stringified = JSON.stringify(response.data)
                this.reassignUpdatedElementIntoList(this.events, response.data)
                this.event = JSON.parse(stringified)
                this.copiedEvent = JSON.parse(stringified)
                alert(stringified);

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
            // Idea : If there is a file, send it. If it is undefined, set it to ''.
            // If it is a file path, we can send it to the backend without any issues.
            
            let field = attachment_file_field

            if (this.fileObjectExists(field))
                return field.files[0].file
            
            if (typeof field === 'undefined')
                return ''

            return field
        },

        reassignUpdatedElementIntoList(list, element){
            // console.log(list)
            // console.log(element)
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

        _skills_custom_label({id, title}){
            
            if (id === '' || Object.is(id,  null)){
                return 'Select'
            }
            else if (Object.is(title, null) || typeof title === 'undefined'){
                
                for (let i = 0; i < this.skillTable.length; ++i){
                    if (this.skillTable[i].id === id){
                        let temp = this.skillTable[i]
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.title}`
                    }
                }
            }
            
            return `${id} ${title}`
            
            
        },

        _staffs_custom_label({id, university_id, firstname, lastname}){

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

        fileObjectExists(field){
            // We want to check if the field contains a file.
            // We need this function because the current file input field is weird 
            // but we need (want) to rely on the form compatability. (vue-formulate)
            let result = false
            if (typeof field === 'undefined' || typeof field === 'null')
                result = false
            else if (typeof field === 'string')
                result = false
            else if (field.files.length === 0)
                result = false
            else
                result = true
                
            return result
        },
        
        attachment_file_max_file_size_validation_function(){
            //Idea : If the file exists, the size must be valid.
            
            let maxFileSize = this.formConstraints.attachment_file.max_file_size.size

            let field = this.event.attachment_file
            if (this.fileObjectExists(field))
                return field.files[0].file.size < maxFileSize
            else
                return true

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
        _generate_formRender(){
            //Generate edit
            let user = this.user
            let edit_info = {}
            
            if (user.is_staff){
                edit_info = this.formRenderSpec['staff']['edit']
            } else if (user.is_student){
                edit_info = this.formRenderSpec['student']['edit']
            }
            
            let formRender = {}
            formRender['edit'] = {}

            if (edit_info['mode'] === 'exclude'){
                Object.entries(this.getEmptyEvent()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = ! edit_info.fields.includes(key)
                });
            } else if (edit_info['mode'] === 'include'){
                Object.entries(this.getEmptyEvent()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key)
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender
        },

        async validateForm(){
        
            //Perform validation on the form.
            await this.$formulate.submit('event-formulate-form-1');

            let vue_formulate_valid = this.$refs['event-formulate-form-1'].isValid;
            

            //vee-validate
            // await this.$validator.validate().then((result) => {
            //     return result
            // });

            //We could take the result. But we want to be explicit here.
            // let vee_validate_valid = (!this.veeErrors.has('multiselect-receivers'))

            return vue_formulate_valid 
        },
    },
    
    created: async function () {
        this.event = this.getEmptyEvent()

        if (this.testMode)
            return;

        await axios.get(this.$API_URL + "user")
            .then((response) => {
                this.user = response.data;
                // console.log(this.user)
            });
        this._generate_formRender();

        axios.get(this.$API_URL + "event")
            .then((response) => {
                this.events = response.data;
                // console.log(this.events)
            });

        axios.get(this.$API_URL + "staff")
            .then((response) => {
                this.staffTable = response.data;
                // console.log(this.staffTable)
            });

        axios.get(this.$API_URL + "skillTable")
            .then((response) => {
                this.skillTable = response.data;
                // console.log(this.skillTable)
            });

        },

    mounted: function () {

        window.onload=()=>{
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
                enabled: false,
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
        




        <div class="modal fade" id="edit-info-modal" tabindex="-1" data-bs-backdrop="static" aria-labelledby="edit-info-modal-label"
            aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">

                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="edit-info-modal-label">{{ modalTitle }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">


                                <button v-if="!addingNewEvent && user.is_staff" type="button"
                                    class="btn btn-primary m-2 fload-end" @click="showEventAttendanceModal = true" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
                                    >
                                    Show Attendances
                                </button>
                                
                                <FormulateForm name="event-formulate-form-1" ref="event-formulate-form-1"  #default="{ hasErrors }">
                                    <formulate-input ref="formulate-input-title" type="text" v-model="event.title" label="Title" validation="required|max:100" :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                                    <FormulateInput ref="formulate-input-start_datetime" type="vue-datetime"  datetype="datetime" v-model="event.start_datetime" label="Start" validation="required"  :disabled="modalReadonly || !formRender.edit.start_datetime"></FormulateInput>
                                    <FormulateInput ref="formulate-input-end_datetime" type="vue-datetime"  datetype="datetime" v-model="event.end_datetime" label="End" validation="required|later"  :validation-rules="{ later : ()=>{return Date.parse(event.start_datetime) < Date.parse(event.end_datetime)}}" :validation-messages="{ later : 'End datetime must be later than start datetime.' }"  error-behavior="live" :disabled="modalReadonly || !formRender.edit.end_datetime"></FormulateInput>
                                    <formulate-input ref="formulate-input-info" label="Info" :key="'event-formulate-input-info-' + formKey" type="textarea" v-model="event.info" validation="max:200,length" :readonly="modalReadonly || !formRender.edit.info" validation-name="info"></formulate-input>
                                    
                                    <h3>Skills</h3>
                                    <multiselect v-model="event.skills" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="skillTable" :custom-label="_skills_custom_label" track-by="id" placeholder="Select..." :disabled="modalReadonly || !formRender.edit.skills">
                                    </multiselect>

                                    <h3>Staffs</h3>
                                    <multiselect v-model="event.staffs" :hide-selected="true"  :close-on-select="false" :multiple="true" :options="staffTable" :custom-label="_staffs_custom_label" track-by="id" placeholder="Select..." :disabled="modalReadonly || !formRender.edit.staffs"></multiselect>
                                    
                                    <p></p>
                                    <FormulateInput  ref="formulate-input-approved" v-model="checkboxes" :options="{approved : 'approved'}" type="checkbox" :disabled="modalReadonly || !formRender.edit.approved"></FormulateInput>
                                    <FormulateInput  ref="formulate-input-used_for_calculation" v-model="checkboxes" :options="{used_for_calculation : 'Use for calculation'}" type="checkbox" :disabled="modalReadonly || !formRender.edit.used_for_calculation"></FormulateInput>
                                    <FormulateInput  ref="formulate-input-attachment_link" type="url" v-model="event.attachment_link"                                            
                                            label="Attachment link" placeholder="URL" validation="" :disabled="modalReadonly  || !formRender.edit.attachment_link" >
                                    </FormulateInput>                                           
                                        
                                    <FormulateInput
                                        type="file" ref="formulate-input-attachment_file" name="formulate-input-attachment_file"
                                        :key="'event-formulate-input-attachment_file-' + formKey" v-model="event.attachment_file" label="Attachment file"  
                                        error-behavior="live" validation-event="input" validation="" upload-behavior="delayed" :disabled="modalReadonly || !formRender.edit.attachment_file" >
                                    </FormulateInput>
                                    <button v-if="copiedEvent.attachment_file != '' &&  !Object.is(copiedEvent.attachment_file, null)" type="button" class="btn btn-primary" @click="openNewWindow(copiedEvent.attachment_file)"> File URL </button>
                                    <button v-if="copiedEvent.attachment_file != '' && !Object.is(copiedEvent.attachment_file, null)" type="button" class="btn btn-outline-danger" @click=" copiedEvent.attachment_file=''; event.attachment_file=''" :disabled="modalReadonly"> Remove File </button>

                                        
                                </FormulateForm>
                            
                            

                            </div>

                        </div>
                        
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button id="createButton" type="button" @click="createClick()" v-if="addingNewEvent" class="btn btn-primary">Create</button>
                            <button v-if="!addingNewEvent && !modalReadonly" id="updateButton" type="button" @click="updateClick()" class="btn btn-primary">Update</button>    
                        </div>

                    </div>

                </div>
            </div>
        </div>


    <AttendanceModal v-model="showEventAttendanceModal" :click-to-close="false">
      <template v-slot:title>Event Attendance</template>
      
      <template v-slot:modal-close-text><button type="button" class="btn btn-secondary" @click="showEventAttendanceModal=false" data-bs-toggle="modal" data-bs-target="#edit-info-modal">Close</button></template>
      <EventAttendance :event_id="event.id" :user="user"></EventAttendance>
      <!-- <template v-slot:params><EventAttendance :event_id="event.id"></EventAttendance></template> -->
    </AttendanceModal>

        <div v-if="false" class="modal fade" id="event-attendance-modal" tabindex="-1" data-bs-backdrop="static" aria-labelledby="event-attendance-modal-label"
            aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">

                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="event-attendance-modal-label">Event Attendance</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">
                                
                                <!-- <ATTENDANCE> -->
                                    <EventAttendance :event_id="event.id"></EventAttendance>

                            </div>

                        </div>
                        
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>

                    </div>

                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
::v-deep .modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  margin: 0 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  background: #fff;
}
.modal__title {
  margin: 0 2rem 0 0;
  font-size: 1.5rem;
  font-weight: 700;
}
.modal__close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}
</style>
