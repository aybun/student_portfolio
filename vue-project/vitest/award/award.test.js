/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from "vitest";

import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import flushPromises from "flush-promises";
import Award from "./src/components/award/Award.vue";

import VueFormulate from "@braid/vue-formulate";
import * as VeeValidate from "vee-validate";

const user_staff = {
    is_staff: true,
    is_student: false,
    groups: ["staff"],
    id: 1,
    is_authenticated: true,
    university_id: "623021038-1",
};
const awards = [
    {
        id: 14,
        title: "test",
        rank: 0,
        received_date: "2023-02-24",
        info: "",
        created_by: 4,
        approved: true,
        approved_by: 1,
        used_for_calculation: false,
        attachment_link: "",
        attachment_file: null,
        skills: [{ id: 1 }, { id: 2 }],
        receivers: [{ id: 3 }, { id: 4 }],
        supervisors: [{ id: 2 }, { id: 1 }],
    },
    {
        id: 21,
        title: "test 2",
        rank: 0,
        received_date: "2023-03-02",
        info: "",
        created_by: 1,
        approved: false,
        approved_by: null,
        used_for_calculation: false,
        attachment_link: "",
        attachment_file: null,
        skills: [{ id: 1 }],
        receivers: [{ id: 4 }],
        supervisors: [],
    },
    {
        id: 25,
        title: "test 2222",
        rank: 0,
        received_date: "2023-03-03",
        info: "",
        created_by: 1,
        approved: false,
        approved_by: null,
        used_for_calculation: false,
        attachment_link: "",
        attachment_file: null,
        skills: [],
        receivers: [{ id: 4 }],
        supervisors: [],
    },
];
const studentTable = [
    {
        id: 3,
        university_id: "623021039-1",
        user_id_fk: 2,
        firstname: "Tubtim",
        middlename: "",
        lastname: "Tubtim",
        faculty_role: 2,
        enroll: 1,
    },
    {
        id: 4,
        university_id: "623021039-2",
        user_id_fk: 4,
        firstname: "Tam",
        middlename: "",
        lastname: "Tam",
        faculty_role: 2,
        enroll: 1,
    },
];
const staffTable = [
    {
        id: 2,
        university_id: "623021038-2",
        user_id_fk: 3,
        firstname: "Toto",
        middlename: "",
        lastname: "Toto",
        faculty_role: 1,
    },
    {
        id: 1,
        university_id: "623021038-1",
        user_id_fk: 1,
        firstname: "Tuta",
        middlename: "",
        lastname: "Tuta",
        faculty_role: 1,
    },
];
const skillTable = [
    { id: 1, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 1" },
    { id: 2, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 2" },
    { id: 3, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 3" },
    { id: 4, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 4" },
    { id: 5, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 5" },
    { id: 6, title: "\u0e17\u0e31\u0e01\u0e29\u0e30\u0e17\u0e35\u0e48 6" },
];

let award_formname = "award-formulate-form-1"
let ref_title = award_formname + "-" + "title"
let ref_rank = award_formname + "-" + "rank"
let ref_received_date = award_formname + "-" + "received_date"
let ref_info = award_formname + "-" + "info"
let ref_skills = award_formname + "-" + "skills"
let ref_receivers = award_formname + "-" + "receivers"
let ref_supervisors = award_formname + "-" + "supervisors"
let ref_approved = award_formname + "-" + "approved"
let ref_used_for_calculation = award_formname + "-" + "used_for_calculation"
let ref_attachment_link = award_formname + "-" + "attachment_link"
let ref_attachment_file = award_formname + "-" + "attachment_file"

describe("Test award.", () => {
    //Concurrentcy
    //Set beforEach()???
    //Makesure that they donot mutate the data.??

    it("award-input-field-validation", async () => {
        const localVue = createLocalVue();
        localVue.use(VueFormulate);
        localVue.use(VeeValidate, { errorBagName: "veeErrors" });
        const wrapper = mount(Award, {
            localVue,
            data() {
                return {
                    award: {}, // This is the input
                    testMode: true, //Skill api calls in the award component.

                    user: JSON.parse(JSON.stringify(user_staff)),
                    awards: JSON.parse(JSON.stringify(awards)),
                    studentTable: JSON.parse(JSON.stringify(studentTable)),
                    staffTable: JSON.parse(JSON.stringify(staffTable)),
                    skillTable: JSON.parse(JSON.stringify(skillTable)),
                };
            },
            // created : function(){}
        });

        // const formulate_form = wrapper.vm.$refs[award_formname];

        //Test : title
        const title = wrapper.vm.$refs[ref_title];

        // title : required
        await wrapper.setData({ award: { title: "" } });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain("Title is required.");

        //title : max:100  || the string contains 102 characters.
        await wrapper.setData({
            award: {
                title:
                    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            },
        });
        title.performValidation();
        await flushPromises();
        expect(title.validationErrors).toContain(
            "Title must be less than or equal to 100 characters long."
        );
        //End Test : title

        //Test : rank
        const rank = wrapper.vm.$refs[ref_rank];

        // rank : required
        await wrapper.setData({ award: { rank: "" } });
        rank.performValidation();
        await flushPromises();
        expect(rank.validationErrors).toContain("Rank is required.");

        // rank : number
        await wrapper.setData({ award: { rank: "a" } });
        rank.performValidation();
        await flushPromises();
        expect(rank.validationErrors).toContain("Rank must be a number.");

        // rank : min:0
        await wrapper.setData({ award: { rank: -1 } });
        rank.performValidation();
        await flushPromises();
        expect(rank.validationErrors).toContain("Rank must be at least 0.");
        //End Test : rank

        //Test : received_date
        const received_date = wrapper.vm.$refs[ref_received_date];

        //received_date : required
        await wrapper.setData({ award: { received_date: "" } });
        received_date.performValidation();
        await flushPromises();
        expect(received_date.validationErrors).toContain(
            "Received Date is required."
        );

        //Test : info
        const info = wrapper.vm.$refs[ref_info];

        //received_date : required || 204 chars
        await wrapper.setData({
            award: {
                info: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            },
        });
        info.performValidation();
        await flushPromises();
        expect(info.validationErrors).toContain(
            "Info must be less than or equal to 200 characters long."
        );

        //Test : receivers

        //receivers : required|min:1
        const receivers = wrapper.vm.$refs[ref_receivers];
        await wrapper.setData({ award: { receivers: [] } });
        wrapper.vm.$validator.validateAll(award_formname); //vee-validate's validator.
        await flushPromises();
        expect(wrapper.vm.veeErrors.collect(award_formname + '.' + 'receivers')).toContain(
            "The receivers field is required"
        );

        //Test : attachment_link : NO VALIDATION RULES !!!!
        const attachment_link = wrapper.vm.$refs[ref_attachment_link];
        await wrapper.setData({ award: { attachment_link: "notalink" } });
        attachment_link.performValidation();
        await flushPromises();
        // console.log(attachment_link.validationErrors)
        expect(attachment_link.validationErrors).toContain('Please include a valid url.');

        //Test : attachment_file
        const attachment_file = wrapper.vm.$refs[ref_attachment_file];

        //attachment_file : maxFileSize
        await wrapper.setData({
            award: { attachment_file: { files: [{ file: { size: 2500000 } }] } },
        });
        attachment_file.performValidation();
        await flushPromises();
        console.log(attachment_file.validationErrors)
        expect(attachment_file.validationErrors).toContain(
            "The file size must not exceed 2 mb."
        );
    });

    it("award-form-submission",
        async () => {
            //Working on this.
            //All fields, except one field, are valid. -> Form should not be submitted.

            const localVue = createLocalVue();
            localVue.use(VueFormulate);
            localVue.use(VeeValidate, { errorBagName: "veeErrors" });
            const wrapper = mount(Award, {
                localVue,
                data() {
                    return {
                        award: {}, // This is the input
                        testMode: true, //Skill api calls in the award component.
                        // awardFormHasBeenSubmitted: true,

                        user: JSON.parse(JSON.stringify(user_staff)),
                        awards: JSON.parse(JSON.stringify(awards)),
                        studentTable: JSON.parse(JSON.stringify(studentTable)),
                        staffTable: JSON.parse(JSON.stringify(staffTable)),
                        skillTable: JSON.parse(JSON.stringify(skillTable)),
                    };
                },
                // created : function(){}
            });
            await flushPromises()

            const valid_award_data = { "id": 14, "title": "test", "rank": 0, "received_date": "2023-03-19", "info": "", "created_by": 4, "approved": true, "approved_by": 1, "used_for_calculation": true, "attachment_link": "https://www.google.com/", "attachment_file": null, "skills": [{ "id": 2 }, { "id": 1 }], "receivers": [{ "id": 2 }], "supervisors": [{ "id": 3 }, { "id": 1 }] }

            let invalids = {
                'title': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                'rank': 'a',
                'received_date': '',
                'info': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                'receivers': [],
                'attachment_link': 'notalink',
                'attachment_file' : { files: [{ file: { size: 2500000 } }]  },
            }
            
            // Test : valid data.
            wrapper.setData({
                award: JSON.parse(JSON.stringify(valid_award_data)),
            });

            await flushPromises()
            // wrapper.vm.testLog()
            // console.log(wrapper.vm.testLog())
            wrapper.vm.updateClick();
            await flushPromises();
            let temp_bool_val = false
            await wrapper.vm.validateForm().then((result) => {
                temp_bool_val = result;
            });
            expect(temp_bool_val).toBe(true);
            
            for (const [key, value] of Object.entries(invalids)) {

                const copied_award = JSON.parse(JSON.stringify(valid_award_data));
                copied_award[key.toString()] = value;
                // console.log([key, value])
                await wrapper.setData({ award: copied_award });
     
                await flushPromises();

                let formIsValid = true;
                await wrapper.vm.validateForm().then((result) => {
                    formIsValid = result;
                });
                expect(formIsValid).toBe(false);
            }

        });


    it("award-form-edit-staff", async () => {
        const localVue = createLocalVue();
        localVue.use(VueFormulate);
        localVue.use(VeeValidate, { errorBagName: "veeErrors" });
        const wrapper = mount(Award, {
            localVue,
            data() {
                return {
                    award: {}, // This is the input
                    testMode: true, //Skill api calls in the award component.
                    // awardFormHasBeenSubmitted: false,

                    user: JSON.parse(JSON.stringify(user_staff)),
                    awards: JSON.parse(JSON.stringify(awards)),
                    studentTable: JSON.parse(JSON.stringify(studentTable)),
                    staffTable: JSON.parse(JSON.stringify(staffTable)),
                    skillTable: JSON.parse(JSON.stringify(skillTable)),
                };
            },
            // created : function(){}
        });

        await flushPromises();

        let html_title = wrapper.findComponent({ ref: ref_title });
        console.log(html_title.attributes());
        expect(html_title.exists()).toBe(true);
    });
});
