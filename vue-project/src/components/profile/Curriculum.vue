<template>
<div>
    <button type="button"
            class="btn btn-primary m-2 fload-end"
            data-bs-toggle="modal"
            data-bs-target="#edit-info-modal"
            @click="addClick()">
         Add Curriculum
    </button>

    <vue-good-table ref="curriculum-vgt" :columns="vgtColumns" :rows="curriculumns"
            :select-options="{ enabled: false, selectOnCheckboxOnly: true }" :search-options="{ enabled: true }"
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
                <span v-if="props.column.field === 'action'">
                    <button v-if="user.is_staff || user.is_student" type="button" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="viewClick(props.row)">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button v-if="
                        user.is_staff 
                        
                    " type="button" :id="'edit-button-' + props.row.id" class="btn btn-light mr-1"
                        data-bs-toggle="modal" data-bs-target="#edit-info-modal" @click="editClick(props.row)">
                        <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="
                        user.is_staff 
                    " type="button" @click="deleteClick(props.row.id)" class="btn btn-light mr-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </span>

                <span v-else>
                    {{ props.formattedRow[props.column.field] }}
                </span>
            </template>
        </vue-good-table>
    
    <div class="modal fade" id="edit-info-modal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false"
        aria-labelledby="edit-info-modal-label" aria-hidden="true">

        <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content">

                <div class="modal-header">
                    <h5 class="modal-title" id="edit-info-modal-label">{% verbatim block %}{{ modalTitle }}{% endverbatim block %}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>

                <div class="modal-body">

                    <div class="d-flex flex-row bd-highlight mb-3">

                        <div class="p-2 w-50 bd-highlight">
                            <button type="button" class="btn btn-primary m-2 fload-end" v-on:click="openNewWindow('/profile/curriculum-student/' + curriculum.id)">
                                Show Students
                            </button>
                            
                            <FormulateForm name="curriculum-formulate-form-1" ref="curriculum-formulate-form-1">
                                <formulate-input ref="curriculum-formulate-input-title" type="text" v-model="curriculum.th_name"
                                        label="Title" validation="required|max:100"
                                        :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                                <formulate-input ref="curriculum-formulate-input-title" type="text" v-model="curriculum.en_name"
                                    label="Title" validation="required|max:100"
                                    :readonly="modalReadonly || !formRender.edit.title"></formulate-input>
                                <FormulateInput
                                    ref="curriculum-formulate-input-start_date"
                                    type="vue-datetime"
                                    datetype="date"
                                    v-model="curriculum.start_date"
                                    label="End"
                                    validation="required"
                                    error-behavior="live"
                                    :disabled="modalReadonly || !formRender.edit.start_date"
                                    ></FormulateInput>
                                <FormulateInput
                                    ref="curriculum-formulate-input-end_date"
                                    type="vue-datetime"
                                    datetype="date"
                                    v-model="curriculum.end_datetime"
                                    label="End"
                                    validation="required|later"
                                    :validation-rules="{
                                        later: () => {
                                            return (
                                                Date.parse(curriculum.start_date) <
                                                Date.parse(curriculum.end_date)
                                            );
                                        },
                                    }"
                                    :validation-messages="{
                                        later: 'End datetime must be later than start datetime.',
                                    }"
                                    error-behavior="live"
                                    :disabled="modalReadonly || !formRender.edit.end_date"
                                    ></FormulateInput>
                                <formulate-input ref="curriculum-formulate-input-info" label="Info"
                                        :key="'curriculum-formulate-input-info-' + formKey" type="textarea"
                                        v-model="curriculum.info" validation="max:200,length"
                                        :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>
                                <FormulateInput type="file"
                                    :key="'curriculum-formulate-input-attachment_file-' + formKey" ref="curriculum-formulate-input-attachment_file"
                                    name="formulate-input-attachment_file" v-model="curriculum.attachment_file" label="Attachment file"
                                    help="The file size must not exceed 2MB." 
                                    :validation-rules="{
                                        maxFileSize: () => {
                                            return true;
                                        }
                                    }" 
                                    :validation-messages="{
                                        maxFileSize:
                                            formConstraints.attachment_file.max_file_size.validation_message(),
                                    }" 
                                    error-behavior="live" validation-event="input" validation="maxFileSize" upload-behavior="delayed" :disabled="
                                        modalReadonly || !formRender.edit.attachment_file
                                    "></FormulateInput>

                                    
                                    <div>
                                        <h6>Skillgroups</h6>
                                        <multiselect ref="curriculum-multiselect-skillgroups" name="multiselect-skillgroups"
                                            v-model="curriculum.skillgroups" v-validate="'required|min:1'"
                                            data-vv-validate-on="input" data-vv-as="skillgroups"  data-vv-scope="curriculum-formulate-form-1"
                                            :hide-selected="true" :close-on-select="false" :multiple="true" :options="skillgroupTable"
                                            :custom-label="_skillgroups_custom_label" track-by="id" placeholder="Select..."
                                            :disabled="modalReadonly || !formRender.edit.skillgroups">
                                        </multiselect>
                                        <span v-show="veeErrors.has('curriculum-multiselect-skillgroups')" style="color: red">{{  veeErrors.first("curriculum-multiselect-skillgroups") }}</span>
                                    </div>        
                            </FormulateForm>


                        </div>

                    </div>
                    
                    
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Close
                    </button>
                    <button id="createButton" type="button" @click="createClick()" v-if="addingNewCurriculum && !modalReadonly"
                        class="btn btn-primary">
                        Create
                    </button>

                    <button id="updateButton" type="button" @click="updateClick()" v-if="!addingNewCurriculum && !modalReadonly"
                        class="btn btn-primary">
                        Update
                    </button>
                </div>

            </div >
        </div >
    </div >

</div >
</template>


<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import * as bootstrap from "bootstrap";


export default {
    components: {
        VueGoodTable,
        Multiselect
    },

    data(){
        return {
            curriculum:{},
            curriculums:{},


            skillgroupTable:{},

            addingNewCurriculum:false,
            modalTitle:"",
            variables: {
                API_URL: "",
            },
            user:{},
            formRender: {},
            formRenderSpec: {
                staff: {
                    edit: {
                        mode: "exclude",
                        fields: [],
                    },
                },

                student: {
                    edit: {
                        mode: "include",
                        fields: [],
                    },
                },
            },
            
            vgtColumns: [
                {
                    label: "Project ID",
                    field: "id",
                    // tooltip: '',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter This Thing", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Title",
                    field: "title",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter This Thing", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Academic Year",
                    field: "start_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "yyyy",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Start Date",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "Start Date",
                    field: "start_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "dd-mm-yyyy",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter Start Date",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "End Date",
                    field: "end_date",
                    filterable: true,
                    type: "date",
                    dateInputFormat: "yyyy-mm-dd",
                    dateOutputFormat: "dd-mm-yyyy",
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        enabled: true,
                        placeholder: "Filter End Date",
                        filterFn: this.dateRangeFilter,
                    },
                },
                {
                    label: "Approved",
                    field: "approved",
                    thClass: "text-center",
                    tdClass: "text-center",
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
        }
    },

    methods: {

        getEmptyCurriculum(){
            return {
                id : 0,
                th_name : '',
                en_name : '',
                start_date : '',
                end_date : '',
                info : '',
                attachment_file : '',

                skillgroups : [],
                
            }
        },
        refreshData(){
            axios.get(this.variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });
        },

        addClick(){
            this.modalTitle="Add Curriculum"
            this.addingNewCurriculum = true // Signal that we are adding a new event -> Create Button.
            this.modalReadonly = false;

            this.assignDataToCurriculumForm(this.getEmptyCurriculum());

        },

        editClick(curriculum){
            this.modalTitle="Edit Curriculum"
            this.addingNewCurriculum = false
            this.modalReadonly = false;

            this.assignDataToCurriculumForm(curriculum);
        },
        assignDataToCurriculumForm(curriculum) {
            const stringified = JSON.stringify(curriculum);
            this.curriculum = JSON.parse(stringified);
            this.copiedCurriculum = JSON.parse(stringified);

        },
        async createClick(){
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof testMode !== "undefined")
                this.curriculumFormHasbeenSubmitted = formIsValid;

            if (!formIsValid) return;


            let outForm = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outForm.append(key.toString(), value)
            }
            outForm.set("skillgroups", JSON.stringify(this.cleanManyToManyFields(this.curriculum.skillgroups)));
            outForm.set("attachment_file", this.cleanAttachmentFile(this.curriculum.attachment_file));

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL+"curriculum",
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

        updateClick(){
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof testMode !== "undefined")
                this.curriculumFormHasbeenSubmitted = formIsValid;

            if (!formIsValid) return;

            let outDict = new FormData();
            for (const [key, value] of Object.entries(this.curriculum)) {
                outDict.append(key.toString(), value)
            }
            outForm.set("skillgroups", JSON.stringify(this.cleanManyToManyFields(this.curriculum.skillgroups)));
            outForm.set("attachment_file", this.cleanAttachmentFile(this.curriculum.attachment_file));

            //Make a request.
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'put',
                url: variables.API_URL+"curriculum/" + this.curriculum.id,
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

        deleteClick(curriculum_id){
            if(!confirm("Are you sure?")){
                return;
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'delete',
                url: variables.API_URL+"curriculum/"+ curriculum_id,
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

        async validateForm(){
            //Perform validation on the form.
            await this.$formulate.submit("curriculum-formulate-form-1");

            const vue_formulate_valid = this.$refs["curriculum-formulate-form-1"].isValid;

            //vee-validate  scope : curriculum
            let vee_validate_valid = false;
            await this.$validator.validateAll("curriculum-formulate-form-1").then((result) => {
                vee_validate_valid = result;
            });

            return vue_formulate_valid && vee_validate_valid;
        }

        onFileSelected(event){
            this.curriculum.attachment_file = event.target.files[0]
        },
        openNewWindow(url){
            window.open(url);
        },
        _generate_formRender() {
            //Generate edit
            let getEmptyObjectFunction = this.getEmptyCurriculum

            const user = this.user;
            let edit_info = {};

            if (user.is_staff) {
                edit_info = this.formRenderSpec["staff"]["edit"];
            } else if (user.is_student) {
                edit_info = this.formRenderSpec["student"]["edit"];
            }

            const formRender = {};
            formRender["edit"] = {};

            if (edit_info["mode"] === "exclude") {
                Object.entries(getEmptyObjectFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(getEmptyObjectFunction()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },
    },

    created: function(){
        this.curriculum = this.getEmptyCurriculum()

        if (typeof testMode !== 'undefined'){
            this._generate_formRender()
            return;
        }

        this.variables.API_URL = this.$API_URL
        axios.get(this.variables.API_URL+"curriculum")
            .then((response)=>{
                this.curriculums=response.data;
            });

        axios.get(this.variables.API_URL+"skillgroup")
            .then((response)=>{
                this.skillgroupTable=response.data;
            });

    },

    mounted:function(){
        window.onload = () => {
            const inputs = [
                'input[placeholder="Filter Start Date"]',
                'input[placeholder="Filter End Date"]',
                // 'input[placeholder="Filter Need By Date"]'
            ];
            
            inputs.forEach(function (input) {
                flatpickr(input, {
                    dateFormat: "d-m-Y",
                    mode: "range",
                    allowInput: true,
                    // enableTime:true,
                });
            });

            document
                .getElementById("edit-info-modal")
                .addEventListener("hidden.bs.modal", (event) => {
                    this.veeErrors.clear();
                    this.formKey += 1;
                });
        };
    },
    },
}

</script>