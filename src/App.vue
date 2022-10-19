<template>
    <SiteHeader />
    <main>
        <aside>
            <h1>Choose Category</h1>
            <ul>
                <li :class="routeName === 'Resum\u00e9'.toLowerCase() ? 'current-tab' : ''">
                    <router-link to="/resume">Resum&#x00e9</router-link>
                </li>
                <li class="cv-tab" :class="routeName === 'Cover Letter'.toLowerCase() ? 'current-tab' : ''">
                    <router-link to="/cv">Cover Letter</router-link>
                    <button :disabled="showCopySuccess || loadingCopy" @click.self="copyCoverLetter">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" v-show="!showCopySuccess && !loadingCopy" viewBox="0 0 16 16">
                            <path d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H9.5a1 1 0 0 0-1 1v7.293l2.646-2.647a.5.5 0 0 1 .708.708l-3.5 3.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L7.5 9.293V2a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h2.5a.5.5 0 0 1 0 1H2z"/>
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="#000" v-show="showCopySuccess && !loadingCopy" viewBox="0 0 16 16">
                            <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                        </svg>
                        <div v-show="loadingCopy" class="lds-dual-ring"></div>
                    </button>
                </li>
                <li class="settings-tab" :class="routeName === 'Settings' ? 'current-tab' : ''">
                    <router-link to="/settings">Settings</router-link>
                </li>
            </ul>
            <LoadingScreen />
        </aside>
        <button
            @click="resetAllFields"
            class="resetContainer">

            <img src="reset.png" />
        </button>
        <router-view></router-view>
    </main>
</template>

<script lang="ts">
import SiteHeader from '@/components/SiteHeader.vue';
import LoadingScreen from '@/components/LoadingScreen.vue';
import { computed } from '@vue/reactivity';
import { defineComponent, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';
import clipboardy from 'clipboardy';

export default defineComponent({
    components: {
        SiteHeader,
        LoadingScreen
    },
    methods: {
        setLoading(loading: boolean) {
            this.loadingCopy = loading;
        },
        setShowCopySuccess(success: boolean) {
            this.showCopySuccess = success;
        }
    },
    data() {
        const store = useStore();

        return {
            routeName: computed(() => useRoute().name),
            showCopySuccess: false,
            loadingCopy: false,
            bg: 'black',
            copyCoverLetter: () => {
                this.setLoading(true);

                axios.get("http://localhost:8000/copy", {
                    params: {
                        nameOfRole: store.state.coverLetter.nameOfRole,
                        companyName: store.state.coverLetter.companyName,
                        recruiterName: !store.state.coverLetter.useCustomRecruiterName ?
                            'Corporate Recruiter' : store.state.coverLetter.recruiterName,
                        coverLetterContent: store.state.settings.coverLetterContent
                    }
                }).then((response) => {
                    this.setLoading(false);
                    clipboardy.write(response.data.contents)
                        .then(() => {
                            this.setShowCopySuccess(true);
                            setTimeout(() => {
                                this.setShowCopySuccess(false)
                            }, 3000);
                        }).catch((e: any) => {
                            this.setShowCopySuccess(false);
                            console.error(e);
                        });
                }).catch((e) => {
                    this.setLoading(false);
                    this.setShowCopySuccess(false);
                    console.error(e);
                });
            },
            resetAllFields() {
                // Resume reset
                store.state.resume.relevantSkills = [];
                store.state.resume.competency = 'Microservices';

                // Cover letter reset
                store.state.coverLetter.nameOfRole = "";
                store.state.coverLetter.companyName = "";
                store.state.coverLetter.recruiterName = "";
                store.state.coverLetter.useCustomRecruiterName = false;

                // Settings reset
                store.state.settings.applicantRole = 'Software Engineer';
                store.state.settings.coverLetterContent = 'Default';
                store.state.settings.graduationMonth = 'August';
                store.state.settings.graduationYear = '2022';
            }
        }
    }
});
</script>

<style lang="scss" scoped>
main {
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: 0 100px;
    width: 80%;
    height: 100%;
    margin: 75px auto 0;
    max-width: 1200px;

    aside {
        width: 100%;
        height: 100%;

        h1 {
            font-size: 2rem;
            margin-bottom: 50px;
        }

        ul {

            li {
                width: 100%;
                border-radius: 20px;
                display: flex;
                transform: translateX(-30px);
                transition: background 150ms ease;

                a {
                    width: 100%;
                    padding: 30px 0;
                    font-weight: 300;
                    font-size: 1.25rem;
                    color: #000;
                    opacity: 0.35;
                    padding-left: 30px;
                    background: transparent;
                    text-align: left;
                    border: none;
                    transition: opacity 150ms ease;
                }

                a.router-link-active {
                    opacity: 1.0;
                }
            }

            li.settings-tab {
                position: relative;
                top: 100px;
            }

            li.cv-tab {

                button {
                    width: 35px;
                    height: 35px;
                    position: relative;
                    margin: auto 0;
                    left: -50px;
                    opacity: 0.0;
                    transition: opacity 150ms ease;
                    pointer-events: none;
                    border: none;
                    background: transparent;

                    svg {
                        pointer-events: none;
                    }
                }

                .lds-dual-ring {
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                }

                .lds-dual-ring:after {
                    content: " ";
                    display: block;
                    width: 16px;
                    height: 16px;
                    border-radius: 50%;
                    border: 1px solid #fff;
                    border-color: #000 transparent #000 transparent;
                    animation: lds-dual-ring 0.5s linear infinite;
                }

                @keyframes lds-dual-ring {
                    0% {
                        transform: rotate(0deg);
                    }
                    100% {
                        transform: rotate(360deg);
                    }
                }

                button:disabled {
                    cursor: none;
                }
            }

            li.cv-tab.current-tab {

                button {
                    opacity: 1.0;
                    pointer-events: unset;
                    transition: opacity 250ms ease;
                }

                button:not(:disabled):hover {
                    opacity: 0.35;
                }
            }

            li.current-tab {
                background-color: rgba(200, 200, 200, 0.1);
            }

            li:not(:last-child) {
                margin-bottom: 15px;
            }
        }
    }

    .resetContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        bottom: 40px;
        right: 40px;
        border-radius: 50px;
        width: 60px;
        height: 60px;
        opacity: 0.25;
        background: none;
        border: none;
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
        transition: opacity 200ms ease;

        img {
            width: 30px;
            height: 30px;
        }

        &:hover{
            opacity: 1.0;
        }
    }
}

footer.copy-dialog {
    display: none;
    justify-content: center;
    align-items: center;
    position: fixed;
    margin: 0 auto;
    bottom: 30px;
    width: 100%;

    p {
        text-align: center;
        font-size: 1rem;
        width: 60%;
        max-width: 800px;
        background-color: rgb(230, 230, 230);
        padding: 30px 0;
        border-radius: 15px;
        color: #000;
    }
}

footer.copy-dialog.show-dialog {
    display: flex;
}
</style>
