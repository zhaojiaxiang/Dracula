<template>
    <div class="body-color">
        <el-row>
            <el-col :xs="22" :sm="22" :md="22" :lg="22" :xl="22">
                <div>
                    <CheckoutList ref="CheckoutList"></CheckoutList>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import CheckoutList from "./components/CheckoutList";
    export default {
        name: "Checkouts",
        components: {
            CheckoutList,
        },
    };
</script>

<style scoped>
    .el-row {
        margin: 0px;
    }
</style>
