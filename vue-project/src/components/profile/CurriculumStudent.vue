<template>
    <div>
        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#addByFileModal">
            Add student by csv file
        </button>

        <vue-good-table ref="curriculum-student-vgt" :columns="vgtColumns" :rows="students"
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
                        <a class="dropdown-item" v-for="(column, index) in vgtColumns" :key="column.label + '-' + index" href="#">
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
                    <button v-if="user.is_staff" type="button" class="btn btn-light mr-1"
                        @click="viewClick(props.row); showAddEventAttendanceModal = true">
                        <i class="bi bi-eye"></i>
                    </button>

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

        <AddAttendanceModal v-model="showAddByFileModal" :click-to-close="false" @closed="_on_add_by_file_modal_closed">
            <template v-slot:modal-close-text><button type="button" class="btn btn-secondary"
                    @click="showAddByFileModal = false">
                    Close
                </button></template>
            <FormulateForm name="curriculum-student-formulate-form-add-by-file" ref="curriculum-student-formulate-form-add-by-file">
                <FormulateInput type="file" :key="'curriculum-student-formulate-form-add-by-file-csvFile-' + addByFileForm.formKey"
                
                    ref="curriculum-student-formulate-form-add-by-file-csvFile"
                    name="curriculum-student-formulate-form-add-by-file-csvFile" v-model="addByFileForm.csvFile"
                    label="Attachment file"
                    :validation-rules="{ maxFileSize :  (context, ... args) => { return context.value.files[0].file.size < parseInt(args[0]);}}"
                                        
                    :validation-messages="{ maxFileSize : (context) => {
                        return 'The file size must not exceed ' + context.args[0] + ' bytes.';},                                     
                    }"
                    error-behavior="live" 
                    validation-event="input" validation="required|maxFileSize" upload-behavior="delayed"
                    :disabled="false">
                </FormulateInput>
                <FormulateInput ref="event-attendance-formulate-input-all-valid-checkbox" v-model="addByFileForm.checkboxes"
                    :options="{ all_must_valid: 'All rows must be valid' }" type="checkbox" :disabled="false">
                </FormulateInput>

                <button type="button" @click="bulkAddClick()" class="btn btn-primary">
                    Process
                </button>
            </FormulateForm>
        </AddAttendanceModal>

    </div>
</template>


<script>
import { Multiselect } from "vue-multiselect";
import { VueGoodTable } from "vue-good-table";
import axios from "axios";

import * as bootstrap from "bootstrap";

import { $vfm, VueFinalModal, ModalsContainer } from "vue-final-modal";

import AddAttendanceModal from "/src/components/event/AddAttendanceModal.vue";

export default {

    components: {
        VueGoodTable,
        Multiselect,
        VueFinalModal,

        AddAttendanceModal,
    },

    props: ["curriculum_id", "user"],

    data() {
        return {
            curriculum_id: 0,
            students: [],

            showAddByFileModal=false,

            modalTitle: '',
            
            addByFileForm: {
                csvFile: "",
                all_must_valid: true,
                checkBoxes: ["all_must_valid"],

                //Do not need reset
                checkboxFields: ["all_must_valid"],
                formKey: 1,
            },
        }
    },

    methods: {
        refreshData() {
            axios.get(variables.API_URL + "student",
                { params: { curriculum_id: this.curriculum_id } })
                .then((response) => {
                    this.students = response.data;
                })

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

            let outDict = {
                'curriculum_id': this.curriculum_id,
                'csv_file': this.csv_file,
            }

            let outForm = new FormData();
            for (const [key, value] of Object.entries(outDict)) {
                outForm.append(key.toString(), value)
            }

            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios({
                method: 'post',
                url: variables.API_URL + "curriculum-student-bulk-add",
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                data: outForm,
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': 'csrftoken',
                }
            }).then((response) => {
                this.refreshData();
                alert(response.data);

            })
        },
        async validateAddByFileForm() {
            await this.$formulate.submit("curriculum-student-formulate-form-add-by-file");

            const vue_formulate_valid =
                this.$refs["curriculum-student-formulate-form-add-by-file"].isValid;

            return vue_formulate_valid;
        },
        _on_add_by_file_modal_closed() {
            this.addByFileForm.formKey += 1;

            this.addByFileForm.csvFile = "";
            this.addByFileForm.all_must_valid = true;
            this.addByFileForm.checkboxes = ["all_must_valid"];
        },
    },

    watch: {
        curriculum_id: function (new_curriculum_id, old_curriculum_id) {
            this.refreshData();
        },
    },
    created: function () {

        axios.get(variables.API_URL + "student", { params: { curriculum_id: this.curriculum_id } })
            .then((response) => {
                this.students = response.data;
            });

    },

    mounted: function () {

    },
}


</script>