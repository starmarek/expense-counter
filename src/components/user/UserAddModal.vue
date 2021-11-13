<template>
    <div class="modal-card">
        <ValidationObserver ref="observer" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(submit)">
                <header class="modal-card-head">
                    <p class="modal-card-title">Create new user</p>
                </header>
                <section class="modal-card-body" style="text-align: left">
                    <ValidatedBInput
                        rules="required|backend-val:auth,User,username"
                        :debounce="500"
                        type="text"
                        label="Username"
                        v-model="username"
                    ></ValidatedBInput>
                    <ValidatedBInput
                        rules="required"
                        type="text"
                        label="First Name"
                        v-model="firstName"
                    ></ValidatedBInput
                    ><ValidatedBInput
                        rules="required"
                        type="text"
                        label="Last Name"
                        v-model="lastName"
                    ></ValidatedBInput>
                </section>
                <footer class="modal-card-foot">
                    <b-button label="Close" @click="$parent.close()" />
                    <b-button label="Create" type="is-primary" native-type="submit" />
                </footer>
            </form>
        </ValidationObserver>
    </div>
</template>
<script>
import { ValidationObserver } from "vee-validate";

export default {
    name: "UserAddModal",
    components: {
        ValidationObserver,
    },
    data: () => ({
        username: "",
        firstName: "",
        lastName: "",
    }),
    methods: {
        submit() {
            this.$store
                .dispatch("user/addUser", {
                    username: this.username,
                    first_name: this.firstName,
                    last_name: this.lastName,
                    password: "foo",
                })
                .then(() => {
                    this.$parent.close();
                })
                .catch((err) => {
                    console.error(err);
                });
        },
    },
};
</script>
