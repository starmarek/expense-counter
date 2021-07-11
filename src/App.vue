<template>
    <div class="wrapper">
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
<style scoped>
.wrapper {
    display: flex;
}
</style>
