<template>
    <div class="is-flex">
        <Sidebar />
        <router-view />
    </div>
</template>
<script>
import Sidebar from "@/components/Sidebar";

export default {
    name: "Home",
    components: { Sidebar },
};
</script>
