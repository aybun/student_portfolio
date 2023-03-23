<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

// import flatpickr from 'flatpickr'
// import 'flatpickr/dist/flatpickr.min.css'
import * as bootstrap from "bootstrap";

import { $vfm, VueFinalModal, ModalsContainer } from "vue-final-modal";

// import AttendanceModal from "/src/components/event/AttendanceModal.vue"
import AddAttendanceModal from "/src/components/event/AddAttendanceModal.vue";

export default {
    components: {
        VueGoodTable,
        Multiselect,
        VueFinalModal,

        AddAttendanceModal,
    },

    props: ["event_id", "user"],

    data() {
        return {
            // user:{},
            modalTitle: "",
            addingNewAttendance: false,
            addByFileModalActive: true, //To reset the behavior of the modal.

            multiselect: {
                // student : {university_id:''}, //multiselect will treat this as a dict.
                student: "",
            },

            formKey: 1,
            eventAttendance: {},
            // event_id: 0,

            studentTable: [],

            showAddEventAttendanceModal: false,
            showAddByFileModal: false,

            addByFileForm: {
                csvFile: "",
                all_must_valid: true,
                checkBoxes: ["all_must_valid"],

                //Do not need reset
                checkboxFields: ["all_must_valid"],
                formKey: 1,
            },

            eventAttendances: [],

            checkboxes: [],
            checkboxFields: ["used_for_calculation"],

            vgtColumns: [
                {
                    label: "Attendance Id",
                    field: "id",
                    // tooltip: 'A simple tooltip',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "University Id",
                    field: "university_id",
                    // tooltip: 'A simple tooltip',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Firstname",
                    field: "firstname",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Lastname",
                    field: "lastname",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        // filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Synced",
                    field: "synced",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip : "รหัสนักศึกษาอยู่ในฐานข้อมูล",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "All", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [true, false], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnApprovedFilterFn, //custom filter function that
                        trigger: "enter", //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Passed",
                    field: "used_for_calculation",
                    thClass: "text-center",
                    tdClass: "text-center",
                    tooltip : "ผ่านการทดสอบ (used_for_calculation)",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "All", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [true, false], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnApprovedFilterFn, //custom filter function that
                        trigger: "enter", //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Action",
                    field: "action",
                    thClass: "text-center",
                    tdClass: "text-center",
                },
            ],
        };
    },

    methods: {
        getEmptyEventAttendance() {
            return {
                id: 0,
                event_id_fk: "",
                university_id: "",

                firstname: "",
                middlename: "",
                lastname: "",

                user_id_fk: "",
                synced: false,

                used_for_calculation: false,
            };
        },

        refreshData() {
            axios
                .get(this.$API_URL + "event-attendance/" + this.event_id)
                .then((response) => {
                    this.eventAttendances = response.data;
                    // console.log(this.eventAttendances)
                });
        },
        addClick() {
            this.modalTitle = "Add Student";
            this.addingNewAttendance = true; // Signal that we are adding a new student -> Create Button.

            this.eventAttendance = this.getEmptyEventAttendance();
            // this.multiselect.student = {'university_id':''}
            this.multiselect.student = null;
        },
        editClick(attendance) {
            this.modalTitle = "Edit Student";
            this.addingNewAttendance = false;

            this.multiselect.student = { university_id: attendance.university_id };
            
            this.eventAttendance = attendance;
            this.checkboxes = [];
            
            for (let i = 0; i < this.checkboxFields.length; ++i) {
                if (this.eventAttendance[this.checkboxFields[i]])
                    this.checkboxes.push(this.checkboxFields[i]);
            }
        },

        createClick() {
            for (let i = 0; i < this.checkboxFields.length; ++i)
                this.eventAttendance[this.checkboxFields[i]] = this.checkboxes.includes(
                    this.checkboxFields[i]
                );

            this.eventAttendance.university_id =
                this.multiselect.student.university_id;
            
            const outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value);
            }
            outDict.set("event_id_fk", this.event_id);

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "event-attendance/",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },
        updateClick() {
            for (let i = 0; i < this.checkboxFields.length; ++i)
                this.eventAttendance[this.checkboxFields[i]] = this.checkboxes.includes(
                    this.checkboxFields[i]
                );

            this.eventAttendance.university_id =
                this.multiselect.student.university_id;
            console.log(this.eventAttendance);
            const outDict = new FormData();
            for (const [key, value] of Object.entries(this.eventAttendance)) {
                outDict.append(key.toString(), value);
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url:
                    this.$API_URL +
                    "event-attendance/" +
                    this.event_id +
                    "/" +
                    this.eventAttendance.id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        deleteClick(attendance_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url:
                    this.$API_URL +
                    "event-attendance/" +
                    this.event_id +
                    "/" +
                    attendance_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        syncByUniversityIdClick() {
            const outDict = {
                event_id: this.event_id,
            };

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url:
                    this.$API_URL + "sync-attendance-by-university-id/" + this.event_id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outDict,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        onCSVFileSelected(event) {
            this.csv_file = event.target.files[0];
        },
        async bulkAddClick() {
            let formIsValid = false;
            await this.validateAddByFileForm().then((result) => {
                formIsValid = result;
            });

            if (!formIsValid) return;

            const form = this.addByFileForm;
            for (let i = 0; i < form.checkboxFields.length; ++i) {
                const fieldName = form.checkboxFields[i];
                form[fieldName] = form.checkboxes.includes(fieldName);
            }

            const outDict = {
                event_id: this.event_id,
                csv_file: this.cleanAttachmentFile(form.csvFile),
                all_must_valid: form.all_must_valid,
            };
            console.log(outDict);
            const outForm = new FormData();
            for (const [key, value] of Object.entries(outDict)) {
                outForm.append(key.toString(), value);
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.$API_URL + "event-attendance-bulk-add",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            })
                .then((response) => {
                    this.refreshData();
                    alert(response.data.message + "\n" + response.data.invalid_rows);
                })
                .catch((error) => {
                    this.refreshData();
                    console.log(error.response.data.message);
                    console.log(error.response.data.invalid_rows);
                    alert(
                        error.response.data.message +
                        "\n" +
                        error.response.data.invalid_rows
                    );
                    // alert(response.message)
                    // alert(response.invalid_rows)
                    // alert(response.message)
                });
        },
        _university_id_custome_label({ university_id, firstname, lastname }) {
            if (
                university_id === "" ||
                Object.is(university_id, null) ||
                typeof university_id === "undefined"
            )
                return "select...";
            else {
                for (let i = 0; i < this.studentTable.length; ++i) {
                    if (this.studentTable[i].university_id === university_id) {
                        const temp = this.studentTable[i];
                        return `${temp.university_id} ${temp.firstname} ${temp.lastname}`;
                    }
                }
                //Not Found
                return "select...";
            }
        },

        cleanAttachmentFile(attachment_file_field) {
            // Idea : If there is a file, send it. If it is undefined, set it to ''.
            // If it is a file path, we can send it to the backend without any issues.
            const field = attachment_file_field;

            const file = this.getFileOrNull(field);
            if (file instanceof File) return file;
            else {
                if (typeof field === "string")
                    //
                    return field;
            }

            if (typeof field === "undefined") return "";

            return field;
        },
        getFileOrNull(field) {
            //We want to support both file and array of files as a field.

            if (field instanceof File) return field;
            else if (typeof field === "undefined" || field === null) return null;
            else if (typeof field === "string") return null;
            else if (field.files.length === 0) return null;
            else return field.files[0].file;
        },
        async validateAddByFileForm() {
            await this.$formulate.submit("event-attendance-formulate-form-2");

            const vue_formulate_valid =
                this.$refs["event-attendance-formulate-form-2"].isValid;

            return vue_formulate_valid;
        },

        _on_add_attendance_modal_closed() {
            this.eventAttendance = this.getEmptyEventAttendance();
        },
        _on_add_by_file_modal_closed() {
            this.addByFileForm.formKey += 1;

            this.addByFileForm.csvFile = "";
            this.addByFileForm.all_must_valid = true;
            this.addByFileForm.checkboxes = ["all_must_valid"];
        },
        toggleColumn(index, event) {
            // Set hidden to inverse of what it currently is
            this.$set(
                this.vgtColumns[index],
                "hidden",
                !this.vgtColumns[index].hidden
            );
        },
    },

    watch: {
        event_id: function (new_event_id, old_event_id) {
            this.refreshData();
        },
    },

    created: function () {
        // console.log(this.user)
        axios.get(this.$API_URL + "student").then((response) => {
            this.studentTable = response.data;
        });
    },
    mounted: function () {
        // this.event_id = JSON.parse(document.getElementById('event_id-data').textContent);
        // console.log(this.event_id)
        // this.refreshData()
    },
};
</script>

<template>
    <div>
        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="
            addClick();
        showAddEventAttendanceModal = true;
                  ">
            Add Student to The Event
        </button>

        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="syncByUniversityIdClick()">
            Sync by university id
        </button>
        
        <button v-if="user.is_staff" type="button" class="btn btn-primary m-2 fload-end" @click="showAddByFileModal = true">
            Add attendees by file
        </button>

        <vue-good-table ref="event-attendance-vgt" :columns="vgtColumns" :rows="eventAttendances"
            :select-options="{ enabled: user.is_staff, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
            :pagination-options="{
                enabled: true,
                mode: 'records',
                perPage: 20,
                setCurrentPage: 1,
            }">
            <div slot="table-actions">
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        columns
                    </button>

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="column.label + '--'+index" href="#">
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
                    <!-- <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1"
                            @click="viewClick(props.row); showAddEventAttendanceModal = true">
                            <i class="bi bi-eye"></i>
                        </button> -->

                    <button v-if="user.is_staff" type="button" :id="'edit-button-' + props.row.id"
                        class="btn btn-light mr-1" @click="
                            editClick(props.row);
                        showAddEventAttendanceModal = true;
                                        ">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="user.is_staff" type="button" @click="deleteClick(props.row.id)"
                        class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>

        <AddAttendanceModal v-model="showAddEventAttendanceModal" :click-to-close="false" :hide-overlay="false"
            :lock-scroll="true" @closed="_on_add_attendance_modal_closed()">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showAddEventAttendanceModal = false">
                    Close
                </button></template>
            <FormulateForm name="event-attendance-formulate-form-1" ref="event-attendance-formulate-form-1"
                #default="{ hasErrors }">
                <h6>University Id</h6>
                <div class="multiselect-university_id">
                    <!-- v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="receivers" -->
                    <multiselect ref="event-attendance-multiselect-university_id"
                        name="event-attendance-multiselect-university_id" v-model="multiselect.student"
                        v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="university id"
                        :hide-selected="true" :close-on-select="false" :multiple="false" :options="studentTable"
                        :custom-label="_university_id_custome_label" track-by="university_id" placeholder="Select..."
                        :disabled="false">
                    </multiselect>
                    <span v-show="veeErrors.has('event-attendance-multiselect-university_id')"
                        class="formulate-input-errors" style="color: red">{{
                            veeErrors.first("event-attendance-multiselect-university_id")
                        }}</span>
                </div>

                <formulate-input label="Firstname" ref="event-attendance-formulate-input-firstname" type="text"
                    v-model="eventAttendance.firstname" validation="max:40" :readonly="false"></formulate-input>
                <formulate-input label="Middlename" ref="event-attendance-formulate-input-middlename" type="text"
                    v-model="eventAttendance.middlename" validation="max:40" :readonly="false"></formulate-input>
                <formulate-input label="Lastname" ref="event-attendance-formulate-input-lastname" type="text"
                    v-model="eventAttendance.lastname" validation="max:40" :readonly="false"></formulate-input>
                <formulate-input ref="event-attendance-formulate-input-used_for_calculation" type="checkbox"
                    v-model="checkboxes" :options="{ used_for_calculation: 'Use for calculation' }" validation=""
                    :readonly="false"></formulate-input>
            </FormulateForm>
            <button type="button" @click="createClick()" v-if="addingNewAttendance" class="btn btn-primary">
                Create
            </button>
            <button type="button" @click="updateClick()" v-else class="btn btn-primary">
                Update
            </button>
        </AddAttendanceModal>

        <AddAttendanceModal v-model="showAddByFileModal" :click-to-close="false" @closed="_on_add_by_file_modal_closed">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showAddByFileModal = false">
                    Close
                </button></template>
            <FormulateForm name="event-attendance-formulate-form-2" ref="event-attendance-formulate-form-2">
                <FormulateInput type="file" :key="
                    'event-attendance-formulate-form-2-attachment_file-' +
                    addByFileForm.formKey
                " ref="event-attendance-formulate-form-2-attachment_file"
                    name="event-attendance-formulate-form-2-attachment_file" v-model="addByFileForm.csvFile"
                    label="Attachment file" help="" 
                    :validation-rules="{ 
                        maxFileSize :  (context, ... args) => {
                            if (getFileOrNull(context.value) !== null)
                                return context.value.files[0].file.size < parseInt(args[0]);
                            return true;
                        },           
                    }"
                    :validation-messages="{
                        maxFileSize: (context) => {
                            return 'The file size must not exceed ' + context.args[0] + ' bytes.';
                        },
                    }" error-behavior="live" validation-event="input" validation="required|maxFileSize" upload-behavior="delayed"
                    :disabled="false">
                </FormulateInput>
                <FormulateInput ref="event-attendance-formulate-form-2-all-valid-checkbox"
                    v-model="addByFileForm.checkboxes" :options="{ all_must_valid: 'All rows must be valid' }"
                    type="checkbox" :disabled="false">
                </FormulateInput>

                <button type="button" @click="bulkAddClick()" class="btn btn-primary">
                    Process
                </button>
            </FormulateForm>
        </AddAttendanceModal>
    </div>
</template>

<style scoped>
.multiselect-university_id {
    width: 68%;
}

.formulate-form {
    width: 50%;
}
</style>
