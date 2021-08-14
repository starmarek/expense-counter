<template>
    <ValidationProvider
        :vid="vid"
        :name="$attrs.label"
        :rules="rules"
        v-slot="{ errors, valid }"
    >
        <b-field
            v-bind="$attrs"
            :type="{ 'is-danger': errors[0], 'is-success': valid }"
            :message="errors"
        >
            <template #label>
                {{ $attrs.label }}
                <span v-if="rules.includes('required')" class="has-text-danger">*</span>
            </template>
            <b-select placeholder="Select a subject" v-model="innerValue">
                <slot />
            </b-select>
        </b-field>
    </ValidationProvider>
</template>

<script>
import { ValidationProvider } from "vee-validate";

export default {
    name: "ValidatedBSelect",
    components: {
        ValidationProvider,
    },
    props: {
        vid: {
            type: String,
        },
        rules: {
            type: [Object, String],
            default: "",
        },
        value: {
            type: null,
        },
    },
    data: () => ({
        innerValue: "",
    }),
    watch: {
        innerValue(newVal) {
            this.$emit("input", newVal);
        },
        value(newVal) {
            this.innerValue = newVal;
        },
    },
    created() {
        if (this.value) {
            this.innerValue = this.value;
        }
    },
};
</script>
