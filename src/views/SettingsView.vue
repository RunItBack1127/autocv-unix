<template>
    <article>
        <section class="applicantRoleContainer">
            <div class="titleContainer">
                <h1>Choose Applicant Role</h1>
                <p>Appears at the top of the resume</p>
            </div>
            <div class="applicantRoleInner">
                <button
                    :class="applicantRole === 'Software Engineer' ? 'current-selection' : ''"
                    @click="setApplicantRole('Software Engineer')">Software Engineer</button>
                <button
                    :class="applicantRole === 'Front End Engineer' ? 'current-selection' : ''"
                    @click="setApplicantRole('Front End Engineer')">Front End Engineer</button>
                <button
                    :class="applicantRole === 'Full Stack Engineer' ? 'current-selection' : ''"
                    @click="setApplicantRole('Full Stack Engineer')">Full Stack Engineer</button>
            </div>
        </section>
        <section class="avToggleContainer">
            <div class="titleContainer">
                <h1>Cover Letter Content</h1>
                <p>Changes third paragraph of the cover letter</p>
            </div>
            <div class="avToggleInner">
                <button
                    :class="coverLetterContent === 'Default' ? 'current-selection' : ''"
                    @click.self="setCoverLetterContent('Default')">Default</button>
                <button
                    :class="coverLetterContent === 'Self Driving' ? 'current-selection' : ''"
                    @click.self="setCoverLetterContent('Self Driving')">Self Driving</button>
            </div>
        </section>
        <section class="graduationContainer">
            <div class="titleContainer">
                <h1>Graduation Date</h1>
                <p>Adjusts graduation date for the specific role</p>
            </div>
            <div class="graduationInner">
                <input value="August" />
                <input value="2022" />
            </div>
        </section>
    </article>
</template>

<script lang="ts">
import { computed } from '@vue/reactivity';
import { defineComponent } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

export default defineComponent({
    setup() {
        const store = useStore();

        return {
            applicantRole: computed(() => store.state.settings.applicantRole),
            coverLetterContent: computed(() => store.state.settings.coverLetterContent),
            setApplicantRole: (role: string) => store.state.settings.applicantRole = role,
            setCoverLetterContent: (content: string) => store.state.settings.coverLetterContent = content
        }
    },
    methods: {
        field(e: MouseEvent) {
            const target = e.target as HTMLInputElement;
            target.dispatchEvent(new MouseEvent('dblclick'));
        }
    }
})
</script>

<style lang="scss" scoped>
article {
    margin-bottom: 50px;

    section {

        .titleContainer {

            h1 {
                font-size: 2rem;
            }

            p {
                font-size: 1.25rem;
                font-weight: 300;
                opacity: 0.25;
                margin: 5px 0 30px;
            }
        }

        div {
            display: grid;

            button {
                font-size: 1.2rem;
                padding: 30px 0;
                border-radius: 10px;
                border: 1px solid #000;
                background: transparent;
                opacity: 0.25;
                transition: opacity 200ms ease;
            }
            
            button.current-selection {
                background-color: #000;
                color: #fff;
                opacity: 1.0;
            }
        }

        &:not(:last-child) {
            margin-bottom: 100px;
        }

        &.graduationContainer {

            .graduationInner {
                grid-template-columns: 1fr 1fr;
                gap: 0 30px;

                input {
                    width: 100%;
                    padding: 30px 0;
                    border-radius: 10px;
                    border: 1px solid #000;
                    font-size: 1.2rem;
                    background: #000;
                    text-align: center;
                    color: #fff;
                }
            }
        }
    }

    section.applicantRoleContainer {

        .applicantRoleInner {
            grid-template-columns: 1fr 1fr;
            gap: 40px 30px;
        }
    }

    section.avToggleContainer {

        .avToggleInner {
            grid-template-columns: 1fr 1fr;
            gap: 0 30px;
        }
    }
}
</style>