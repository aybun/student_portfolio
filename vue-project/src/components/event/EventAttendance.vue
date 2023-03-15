<script>
import { Multiselect } from 'vue-multiselect'
import { VueGoodTable } from  'vue-good-table';
import axios from 'axios'

// import flatpickr from 'flatpickr'
// import 'flatpickr/dist/flatpickr.min.css'
import * as bootstrap from 'bootstrap'

import { $vfm, VueFinalModal, ModalsContainer } from 'vue-final-modal'

export default {
    components: {
        VueGoodTable,
        Multiselect,
        VueFinalModal
    },

    props:['event_id'],

    data() {
        return {
            modalTitle: "",
            addingNewStudent: false,
            addByFileModalActive: true, //To reset the behavior of the modal.

            eventAttendance: {},
            event_id: 0,


            showAddAEventAttendanceModal:false,

            csv_file: '',
            eventAttendances: [],

            checkboxes: [],
            checkboxFields: ['used_for_calculation'],

            vgtColumns: [
                {
                    label: 'Attendance Id',
                    field: 'id',
                    // tooltip: 'A simple tooltip',
                    thClass: 'text-center',
                    tdClass: 'text-center',
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
                    label: 'University Id',
                    field: 'university_id',
                    // tooltip: 'A simple tooltip',
                    thClass: 'text-center',
                    tdClass: 'text-center',
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
                    label: 'Firstname',
                    field: 'firstname',
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
                    label: 'Lastname',
                    field: 'lastname',
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
                    label: 'Synced',
                    field: 'synced',
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
        getEmptyEventAttendance() {
            return {
                id: 0,
                event_id_fk: '',
                university_id: '',

                firstname: '',
                middlename: '',
                lastname: '',

                user_id_fk: '',
                synced: false,

                used_for_calculation: false,
            }

        },

        refreshData() {
            axios.get(this.$API_URL + "event-attendance/" + this.event_id)
                .then((response) => {
                    this.eventAttendances = response.data;
                    // console.log(this.eventAttendances)
                });

        },
        addClick() {
            this.modalTitle = "Add Student"
            this.addingNewStudent = true // Signal that we are adding a new student -> Create Button.

            this.eventAttendance = this.getEmptyEventAttendance()
        },
        editClick(attendance) {
            this.modalTitle = "Edit Student";
            this.addingNewStudent = false

            this.eventAttendance = attendance
            this.checkboxes = []

            for (let i = 0; i < this.checkboxFields.length; ++i) {
                if (this.eventAttendance[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i])
            }
        },

        createClick() {

            for (let i = 0; i < this.checkboxFields.length; ++i)
                this.eventAttendance[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value)
            }
            outDict.set('event_id_fk', this.event_id)

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: this.$API_URL + "event-attendance/",
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
            })

        },
        updateClick() {

            for (let i = 0; i < this.checkboxFields.length; ++i)
                this.eventAttendance[this.checkboxFields[i]] = this.checkboxes.includes(this.checkboxFields[i])

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: this.$API_URL + "event-attendance/" + this.event_id + '/' + this.eventAttendance.id,
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
            })
        },

        deleteClick(attendance_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: this.$API_URL + "event-attendance/" + this.event_id + '/' + attendance_id,
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            })
        },

        syncByUniversityIdClick() {

            let outDict = {
                'event_id': this.event_id,
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: this.$API_URL + "sync-attendance-by-university-id/" + this.event_id,
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
            })
        },

        onCSVFileSelected(event) {
            this.csv_file = event.target.files[0]

        },
        bulkAddClick() {

            let outDict = {
                'event_id': this.event_id,
                'csv_file': this.csv_file,
            }

            let outForm = new FormData();
            for (const [key, value] of Object.entries(outDict)) {
                outForm.append(key.toString(), value)
            }
            // outForm.set('event_id_fk', this.event_id)

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: this.$API_URL + "event-attendance-bulk-add",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outForm,
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response) => {
                this.refreshData();
                // console.log(response.data)
                // console.log(response.data.message)
                alert(response.data);
                // alert(response.message);

                //Reset the behavior of the modal.
                this.addByFileModalActive = false
                this.addByFileModalActive = true

            }).catch((error) => {
                this.refreshData();
                console.log(error.response.data.message)
                console.log(error.response.data.invalid_rows)
                alert(error.response.data.invalid_rows)
                    // alert(response.message)
                    // alert(response.invalid_rows)
                    // alert(response.message)
                    ;
            }
            )
        }



    },
    
    watch: {
        event_id: function (new_event_id, old_event_id) {
            this.refreshData()
        },
    },

    created: function () {


    },
    mounted: function () {

        // this.event_id = JSON.parse(document.getElementById('event_id-data').textContent);
        // console.log(this.event_id)
        // this.refreshData()


    },
}
</script>

<template>
    <div>

        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-attendance-info-modal"
            @click="addClick()">
            Add Student to The Event
        </button>

        <button type="button" class="btn btn-primary m-2 fload-end" @click="syncByUniversityIdClick()">
            Sync by university id
        </button>

        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal"
            data-bs-target="#add-by-file-modal-label">
            Add attendees by file
        </button>

        <vue-good-table ref="vgt" :columns="vgtColumns" :rows="eventAttendances"
            :select-options="{ enabled: true, selectOnCheckboxOnly: true, }" :search-options="{ enabled: true }"
            :pagination-options="{ enabled: true, mode: 'records', perPage: 10, setCurrentPage: 1, }"
            >

            <div slot="table-actions">
                <div class="dropdown">

                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        columns
                    </button>

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="index" href="#">

                            <span href="#" class="small" tabIndex="-1" @click.prevent="toggleColumn(index, $event)">
                                <formulate-input type="checkbox" v-if="!column.hidden" disabled="true"
                                    checked="true"></formulate-input>
                                {{ column.label }}
                            </span>

                        </a>
                    </div>

                </div>

            </div>

            <template slot="table-row" slot-scope="props">
                <span v-if="props.column.field == 'action'">

                    <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="viewClick(props.row);">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button
                        v-if="user.is_staff || !props.row.approved && props.row.created_by === user.id && user.is_student"
                        type="button" :id="'edit-button-' + props.row.id" class="btn btn-light mr-1" data-bs-toggle="modal"
                        data-bs-target="#edit-info-modal" @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button
                        v-if="user.is_staff || !props.row.approved && props.row.created_by === user.id && user.is_student"
                        type="button" @click="deleteClick(props.row.id)" class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>

        <div class="modal fade" id="edit-attendance-info-modal" tabindex="-1" aria-labelledby="edit-attendance-info-modal-label" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="edit-attendance-info-modal-abel">{{ modalTitle }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">

                                <!--                        <div class="input-group mb-3" >-->
                                <!--                            <span class="input-group-text">Student Id</span>-->
                                <!--                            <input v-bind:disabled="!addingNewStudent" type="text" class="form-control" v-model="eventAttendance.student_id">-->
                                <!--                        </div>-->

                                <div class="input-group mb-3">
                                    <span class="input-group-text">University Id</span>
                                    <input type="text" class="form-control" v-model="eventAttendance.university_id">
                                </div>

                                <div class="input-group mb-3">
                                    <span class="input-group-text">Firstname</span>
                                    <input type="text" class="form-control" v-model="eventAttendance.firstname">
                                </div>

                                <div class="input-group mb-3">
                                    <span class="input-group-text">Middlename</span>
                                    <input type="text" class="form-control" v-model="eventAttendance.middlename">
                                </div>

                                <div class="input-group mb-3">
                                    <span class="input-group-text">Lastname</span>
                                    <input type="text" class="form-control" v-model="eventAttendance.lastname">
                                </div>

                                <div v-if="!addingNewStudent" class="mb-3">
                                    <input type="checkbox" value="used_for_calculation" v-model="checkboxes" />
                                    <label>&nbsp;Use for calculation</label>

                                </div>

                            </div>

                        </div>
                        <button type="button" @click="createClick()" v-if="addingNewStudent" class="btn btn-primary">
                            Create
                        </button>
                        <button type="button" @click="updateClick()" v-else class="btn btn-primary">
                            Update
                        </button>

                    </div>

                </div>
            </div>
        </div>



        <div v-if="addByFileModalActive" class="modal fade" id="add-by-file-modal" tabindex="-1"
            aria-labelledby="add-by-file-modal-label" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="add-by-file-modal-label">Add By CSV File</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">
                                <div class="mb-3">
                                    <label for="csvFormFile" class="form-label">
                                        <h3>Attachment file</h3>
                                    </label>
                                    <p></p>

                                    <input class="form-control" type="file" id="csvFormFile" @change="onCSVFileSelected"
                                        accept=".csv">

                                </div>

                            </div>

                        </div>

                        <button type="button" @click="bulkAddClick()" class="btn btn-primary">
                            Process
                        </button>

                    </div>

                </div>
            </div>
        </div>



    </div>
</template>