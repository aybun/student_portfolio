<template>
    <div>
        <button type="button" class="btn btn-primary m-2 fload-end" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
            @click="addClick()">
            Add Skillgroup
        </button>

        <vue-good-table ref="skillgroup-vgt" :columns="vgtColumns" :rows="skillgroups"
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
                <span v-if="props.column.field == 'action'">
                    <button v-if="user.is_staff" type="button" class="btn btn-light mr-1" data-bs-toggle="modal"
                        data-bs-target="#edit-info-modal" @click="viewClick(props.row)">
                        <i class="bi bi-eye"></i>
                    </button>

                    <button v-if="user.is_staff" type="button" :id="'edit-button-' + props.row.id"
                        class="btn btn-light mr-1" data-bs-toggle="modal" data-bs-target="#edit-info-modal"
                        @click="editClick(props.row)">
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
        <div class="modal fade" id="edit-info-modal" tabindex="-1" aria-labelledby="edit-info-modal-label"
            aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="edit-info-modal-label">
                            {{ modalTitle }}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <div class="d-flex flex-row bd-highlight mb-3">
                            <div class="p-2 w-50 bd-highlight">
                                <FormulateForm name="skillgroup-formulate-form-1" ref="skillgroup-formulate-form-1">
                                    <formulate-input ref="skillgroup-formulate-input-name" type="text"
                                        v-model="skillgroup.name" label="Name" validation="required|max:100"
                                        :readonly="modalReadonly || !formRender.edit.name"></formulate-input>
                                    <formulate-input ref="skillgroup-formulate-input-info" label="Info"
                                        :key="'skillgroup-formulate-input-info-' + formKey" type="textarea"
                                        v-model="skillgroup.info" validation="max:200,length"
                                        :readonly="modalReadonly || !formRender.edit.info"
                                        validation-name="info"></formulate-input>
                                    <div>
                                        <h6>Skills</h6>
                                        <multiselect v-model="skillgroup.skills" :hide-selected="true"
                                            :close-on-select="false" ref="skillgroup-multiselect-skills"
                                            name="skillgroup-multiselect-skills" :multiple="true" :options="skillTable"
                                            :custom-label="_skills_custom_label" track-by="id" placeholder="Select..."
                                            v-validate="'required|min:1'" data-vv-validate-on="input" data-vv-as="skills"
                                            data-vv-scope="skillgroup" :disabled="modalReadonly || !formRender.edit.skills">
                                        </multiselect>
                                        <span v-show="
                                            veeErrors.has('skillgroup.skillgroup-multiselect-skills')
                                        " style="color: red">{{
    veeErrors.first(
        "'skillgroup.skillgroup-multiselect-skills'"
    )
}}</span>
                                    </div>
                                </FormulateForm>


                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                            <button id="createButton" type="button" @click="createClick()" v-if="addingNewSkillgroup"
                                class="btn btn-primary">
                                Create
                            </button>

                            <button id="updateButton" type="button" @click="updateClick()" v-if="!addingNewSkillgroup"
                                class="btn btn-primary">
                                Update
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
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
        Multiselect,
    },

    data() {
        return {
            skillgroup: {},
            copiedSkillgroup: {},
            skillgroups: [],

            skillTable: [],
            user: {},
            addingNewSkillgroup: false,
            formKey: 1,
            variables: {
                API_URL: "",
            },

            modalTitle: "",
            modalReadonly: false,
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
                    label: "Skillgroup ID",
                    field: "id",
                    // tooltip: '',
                    thClass: "text-center",
                    tdClass: "text-center",
                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter ID", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
                    },
                },
                {
                    label: "Name",
                    field: "name",
                    thClass: "text-center",

                    filterOptions: {
                        styleClass: "class1", // class to be added to the parent th element
                        enabled: true, // enable filter for this column
                        placeholder: "Filter Name", // placeholder for filter input
                        filterValue: "", // initial populated value for this filter
                        filterDropdownItems: [], // dropdown (with selected values) instead of text input
                        // filterFn: this.columnFilterFn, //custom filter function that
                        // trigger: 'enter', //only trigger on enter not on keyup
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
        getEmptySkillgroup() {
            return {
                id: 0,
                name: "",
                info: "",
                skills: "",
            };
        },

        refreshData() {
            axios.get(this.variables.API_URL + "skillgroup").then((response) => {
                this.skillgroups = response.data;
            });
        },

        addClick() {
            this.modalTitle = "Add Skillgroup";
            this.addingNewSkillgroup = true; // Signal that we are adding a new event -> Create Button.
            this.modalReadonly = false;

            this.assignDataToSkillgroupForm(this.getEmptySkillgroup());
        },
        viewClick(skillgroup) {
            this.modalTitle = "View Skillgroup";
            this.addingNewSkillgroup = false;
            this.modalReadonly = true;

            this.assignDataToSkillgroupForm(skillgroup);
        },
        editClick(skillgroup) {
            this.modalTitle = "Edit Skillgroup";
            this.addingNewSkillgroup = false;
            this.modalReadonly = false;

            this.assignDataToSkillgroupForm(skillgroup);
        },
        assignDataToSkillgroupForm(formData) {
            const stringified = JSON.stringify(formData);
            this.skillgroup = JSON.parse(stringified);
            this.copiedSkillgroup = JSON.parse(stringified);
        },
        async createClick() {
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof testMode !== "undefined")
                this.skillgroupFormHasbeenSubmitted = formIsValid;

            if (!formIsValid) return;

            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outForm.append(key.toString(), value);
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "post",
                url: this.variables.API_URL + "skillgroup",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        async updateClick() {
            let formIsValid = false;
            await this.validateForm().then((result) => {
                formIsValid = result;
            });

            if (typeof testMode !== "undefined")
                this.skillgroupFormHasbeenSubmitted = formIsValid;

            if (!formIsValid) return;

            const outForm = new FormData();
            for (const [key, value] of Object.entries(this.skillgroup)) {
                outForm.append(key.toString(), value);
            }
            outForm.set(
                "skills",
                JSON.stringify(this.cleanManyToMantFields(this.skillgroup.skills))
            );

            //Make a request.
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "put",
                url: this.variables.API_URL + "skillgroup/" + this.skillgroup.id,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                data: outForm,
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },

        deleteClick(skillgroup_id) {
            if (!confirm("Are you sure?")) {
                return;
            }

            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios({
                method: "delete",
                url: this.variables.API_URL + "skillgroup/" + skillgroup_id,
                xstfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: {
                    "X-CSRFToken": "csrftoken",
                },
            }).then((response) => {
                this.refreshData();
                alert(response.data);
            });
        },
        cleanManyToManyFields(list) {
            //Remove empty or redundant inputs.
            // console.log(list)
            const nonEmpty = [];
            const ids = [];
            for (let i = 0; i < list.length; ++i) {
                const id = list[i]["id"];

                if (id !== "" && !ids.includes(id)) {
                    ids.push(list[i].id);
                    nonEmpty.push({ id: list[i].id });
                }
            }
            return nonEmpty;
        },

        async validateForm() {
            await this.$formulate.submit("skillgroup-formulate-form-1");

            const vue_formulate_valid =
                this.$refs["skillgroup-formulate-form-1"].isValid;

            //vee-validate :validate the scope : skillgroup
            let vee_validate_valid = false;
            await this.$validator.validateAll("skillgroup").then((result) => {
                vee_validate_valid = result;
            });

            return vue_formulate_valid && vee_validate_valid;
        },
        _generate_formRender() {
            //Generate edit
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
                Object.entries(this.getEmptySkillgroup()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = !edit_info.fields.includes(key);
                });
            } else if (edit_info["mode"] === "include") {
                Object.entries(this.getEmptySkillgroup()).forEach(([key, _]) => {
                    formRender.edit[key.toString()] = edit_info.fields.includes(key);
                });
            } else {
                throw "The mode must be in { exlude, include }.";
            }

            this.formRender = formRender;
        },
        _skills_custom_label({ skill_id_fk, title }) {
            let id = skill_id_fk;
            if (id === "" || id === null || typeof id === "undefined") {
                return "Select";
            } else if (title === null || typeof title === "undefined") {
                for (let i = 0; i < this.skillTable.length; ++i) {
                    if (this.skillTable[i].id === id) {
                        const temp = this.skillTable[i];
                        // console.log('in the loop : ', temp)
                        return `${temp.id} ${temp.title}`;
                    }
                }
            }

            return `${id} ${title}`;
        },

    },
    created: async function () {
        this.skillgroup = this.getEmptySkillgroup();

        if (typeof this.testMode !== "undefined") {
            this._generate_formRender();
            return;
        }
        this.variables.API_URL = this.$API_URL
        await axios.get(this.variables.API_URL + "user").then((response) => {
            this.user = response.data;
        });

        this._generate_formRender();

        axios.get(this.variables.API_URL + "skillgroup").then((response) => {
            this.skillgroups = response.data;
        });

        axios.get(this.variables.API_URL + "skillTable").then((response) => {
            this.skillTable = response.data;
        });
    },

    mounted: function () {
        window.onload = () => {
            const inputs = [
                // 'input[placeholder="Filter Received"]',
                // 'input[placeholder="Filter Start Date"]',
                // 'input[placeholder="Filter Need By Date"]'
            ];

            inputs.forEach(function (input) {
                flatpickr(input, {
                    dateFormat: "Y-m-d",
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
};
</script>
