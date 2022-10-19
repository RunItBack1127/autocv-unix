import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createStore } from 'vuex';
import App from './App.vue';
import '@/style.scss';

import ResumeFormView from '@/views/ResumeFormView.vue';
import CoverLetterFormView from '@/views/CoverLetterFormView.vue';
import SettingsView from '@/views/SettingsView.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: to => {
                return {
                    path: '/resume'
                }
            }
        },
        {
            path: '/resume',
            name: 'Resum\u00e9'.toLowerCase(),
            component: ResumeFormView
        },
        {
            path: '/cv',
            name: 'Cover Letter'.toLowerCase(),
            component: CoverLetterFormView
        },
        {
            path: '/settings',
            name: 'Settings',
            component: SettingsView
        }
    ]
});

const store = createStore({
    state() {
        return {
            resume: {
                relevantSkills: [],
                competency: 'Microservices'
            },
            coverLetter: {
                nameOfRole: '',
                companyName: '',
                recruiterName: '',
                useCustomRecruiterName: false
            },
            settings: {
                applicantRole: 'Software Engineer',
                coverLetterContent: 'Default',
                graduationMonth: 'August',
                graduationYear: 2022
            },
            showLoadingScreen: false
        }
    }
});

createApp(App)
    .use(router)
    .use(store)
    .mount('#app');
