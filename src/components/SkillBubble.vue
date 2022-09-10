<template>
    <span>
        <p>{{ name }}</p>
        <button
            @click.prevent="$emit('modifySkill', {
                method: REMOVE_SKILL,
                skill: name
            })">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
            </svg>
        </button>
    </span>
</template>

<script lang="ts">
import { ModifySkillMethod } from '../util/ModifySkillPayload';

export default {
    props: {
        name: String
    },
    data() {
        return {
            REMOVE_SKILL: ModifySkillMethod.REMOVE
        }
    }
}
</script>

<style lang="scss" scoped>
span {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 90px;
    border-radius: 30px;
    background-color: transparent;
    box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;

    p {
        font-size: 1.1rem;
        color: #000;
    }

    button {
        display: none;
        position: absolute;
        background: transparent;
        border: none;
        margin-left: 7%;

        svg {
            width: 20px;
            height: 20px;
        }
    }
}

span:hover button {
    display: block;
}
</style>