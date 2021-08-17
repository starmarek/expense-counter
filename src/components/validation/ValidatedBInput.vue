<template>
    <ValidationProvider
        :vid="vid"
        :name="$attrs.name || $attrs.label"
        :debounce="$attrs.debounce || 0"
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
            <b-input v-model="innerValue" v-bind="$attrs"></b-input>
        </b-field>
    </ValidationProvider>
</template>

<script>
import { ValidationProvider } from "vee-validate";

export default {
    name: "ValidatedBInput",
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
