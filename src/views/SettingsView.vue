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
                    @click="applicantRole = 'Software Engineer'">Software Engineer</button>
                <button
                    :class="applicantRole === 'Front End Engineer' ? 'current-selection' : ''"
                    @click="applicantRole = 'Front End Engineer'">Front End Engineer</button>
                <button
                    :class="applicantRole === 'Full Stack Engineer' ? 'current-selection' : ''"
                    @click="applicantRole = 'Full Stack Engineer'">Full Stack Engineer</button>
            </div>
        </section>
        <section class="avToggleContainer">
            <div class="titleContainer">
                <h1>Cover Letter Content</h1>
                <p>Changes third paragraph of the cover letter</p>
            </div>
            <div className="avToggleInner">
                <button
                    :class="coverLetterContent === 'Default' ? 'current-selection' : ''"
                    @click.self="coverLetterContent = 'Default'">Default</button>
                <button
                    :class="coverLetterContent === 'Self Driving' ? 'current-selection' : ''"
                    @click.self="coverLetterContent = 'Self Driving'">Self Driving</button>
            </div>
        </section>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    data() {
        return {
            applicantRole: 'Software Engineer',
            coverLetterContent: 'Default'
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
    }

    section.applicantRoleContainer {
        margin-bottom: 85px;

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