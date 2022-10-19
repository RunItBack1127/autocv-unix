<template>
    <form @submit.prevent="onSubmit">
        <div class="skillsDashboardContainer">
            <header>
                <label for="skillsDashboardInput">Update Relevant Skills</label>
                <p>Add 7 relevant technologies.</p>
            </header>
            <SkillsDashboard
                :skills="skills"
                :disabled="skills.length === 7"
                @modify-skill="(payload: ModifySkillPayload) => {
                    if( payload.method === REMOVE_SKILL ) {
                        removeSkill(payload.skill);
                    }
                    else {
                        addSkill(payload.skill);
                    }
                }" />
        </div>
        <div className="competenciesToggleContainer">
            <h1>Select Competency</h1>
            <div className="competenciesToggleInner">
                <input @click.self="setCompetency('Microservices')" :class="competency === 'Microservices' ? 'current-selection' : ''" type="button" value="Microservices" />
                <input @click.self="setCompetency('Databases')" :class="competency === 'Databases' ? 'current-selection' : ''" type="button" value="Databases" />
            </div>
        </div>
        <SubmitResetMenu
            :disabled="skills.length !== 7"
            @reset-form-fields="resetFormFields" />
    </form>
</template>

<script lang="ts">
import SiteHeader from '@/components/SiteHeader.vue';
import SkillsDashboard from '@/components/SkillsDashboard.vue';
import SubmitResetMenu from '@/components/SubmitResetMenu.vue';
import { ModifySkillPayload, ModifySkillMethod } from '../util/ModifySkillPayload';
import { computed } from '@vue/reactivity';
import { defineComponent } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
    components: {
        SiteHeader,
        SkillsDashboard,
        SubmitResetMenu
    },
    data() {
        const store = useStore();

        function capitalize( skill: string ) {
            return `${skill[0].toUpperCase()}${skill.slice(1)}`;
        }

        return {
            REMOVE_SKILL: ModifySkillMethod.REMOVE,
            skills: computed(() => store.state.resume.relevantSkills),
            competency: computed(() => store.state.resume.competency),
            setCompetency: (competency: string) => store.state.resume.competency = competency,
            addSkill: (skill: string) => {
                const addSkill = capitalize( skill );
                if(!store.state.resume.relevantSkills.includes(addSkill)) {
                    store.state.resume.relevantSkills.push(addSkill);
                }
            },
            removeSkill: (skill: string) => {
                const refSkill = capitalize( skill );
                store.state.resume.relevantSkills = store.state.resume.relevantSkills.filter((sk: string) => {
                    return sk !== refSkill;
                });
            },
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

                axios.get("http://localhost:8000/resume", {
                    params: {
                        competency: store.state.resume.competency,
                        relevantSkills: store.state.resume.relevantSkills.join(","),
                        applicantRole: store.state.settings.applicantRole
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
                store.state.resume.relevantSkills = [];
                store.state.resume.competency = 'Microservices';
            },
        }
    }
});
</script>

<style lang="scss" scoped>
form {

    .skillsDashboardContainer {
        header {
            label {
                font-size: 2rem;
                font-weight: 700;
            }

            p {
                font-size: 1.25rem;
                font-weight: 300;
                margin: 5px 0 40px;
                opacity: 0.35;
            }
        }
    }

    .competenciesToggleContainer {
        margin-bottom: 100px;

        h1 {
            margin-bottom: 25px;
        }

        .competenciesToggleInner {
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0 50px;
            
            input[type="button"] {
                font-size: 1.25rem;
                padding: 25px 0;
                border-radius: 10px;
                border: 1px solid #000;
                background: transparent;
                transition: opacity 200ms ease;
                opacity: 0.25;
            }

            input[type="button"].current-selection {
                opacity: 1.0;
            }
        }
    }
}
</style>