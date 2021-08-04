<template>
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">Create new user</p>
        </header>
        <section class="modal-card-body"></section>
        <footer class="modal-card-foot">
            <b-button label="Close" @click="$parent.close()" />
            <b-button label="Create" type="is-primary" />
        </footer>
    </div>
</template>
<script>
// import { mapState, mapActions, mapGetters } from "vuex";

export default {
    name: "UserAddModal",
};
</script>
