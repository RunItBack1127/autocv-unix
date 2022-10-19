<template>
    <form @submit.prevent="onSubmit">
        <BasicFormInput title="Name of Role" subText="Software Engineer" v-model="store.state.coverLetter.nameOfRole" />
        <BasicFormInput title="Company Name" subText="Cruise, LLC" v-model="store.state.coverLetter.companyName" />
        <div class="customRecruiterContainer">
            <label for="customRecruiterCheckbox">Use custom recruiter name?</label>
            <input tabindex="-1" type="checkbox" v-model="store.state.coverLetter.useCustomRecruiterName" />
        </div>
        <BasicFormInput
            title="Recruiter Name"
            subText="Bryan Danielson"
            v-model="store.state.coverLetter.recruiterName"
            :disabled="!store.state.coverLetter.useCustomRecruiterName" />
        <SubmitResetMenu
            :disabled="store.state.coverLetter.nameOfRole === '' ||
                store.state.coverLetter.companyName === '' ||
                (store.state.coverLetter.useCustomRecruiterName
                && store.state.coverLetter.recruiterName === '')"
            @reset-form-fields="resetFormFields" />
    </form>
</template>

<script lang="ts">
import BasicFormInput from '@/components/BasicFormInput.vue';
import SubmitResetMenu from '../components/SubmitResetMenu.vue';
import { defineComponent } from 'vue';
import { storeKey, useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
    components: {
        BasicFormInput,
        SubmitResetMenu
    },
    data() {
        const store = useStore();

        return {
            store,
            setBodyOverflow(overflow: string) {
                const body = document.querySelector('body');
                if( body != null ) {
                    body.style.overflow = overflow;
                }
            },
            onSubmit: (e: Event) => {
                e.preventDefault();
                store.state.showLoadingScreen = true;
                this.setBodyOverflow("hidden");

                const companyName = store.state.coverLetter.companyName;

                axios.get("http://localhost:8000/cv", {
                    params: {
                        recruiterName: !store.state.coverLetter.useCustomRecruiterName ?
                            `${companyName} Hiring Manager` : store.state.coverLetter.recruiterName,
                        companyName,
                        nameOfRole: store.state.coverLetter.nameOfRole,
                        applicantRole: store.state.settings.applicantRole,
                        coverLetterContent: store.state.settings.coverLetterContent
                    }
                }).then((response) => {
                    window.open(response.data.url);
                }).catch((e) => {
                    console.error(e);
                }).finally(() => {
                    store.state.showLoadingScreen = false;
                    this.setBodyOverflow("auto");
                });
            },
            resetFormFields: () => {
                store.state.coverLetter.nameOfRole = "";
                store.state.coverLetter.companyName = "";
                store.state.coverLetter.recruiterName = "";
                store.state.coverLetter.useCustomRecruiterName = false;
            }
        }
    }
})
</script>

<style lang="scss" scoped>
form {

    .customRecruiterContainer {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 100%;

        label {
            font-size: 1.1rem;
            font-weight: 300;
            margin-right: 15px;
            opacity: 0.9;
        }
    }
}
</style>