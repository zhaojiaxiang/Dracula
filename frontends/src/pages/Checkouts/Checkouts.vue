<template>
    <div class="body-color">
        <el-row>
            <el-col :xs="23" :sm="23" :md="23" :lg="23" :xl="23">
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
