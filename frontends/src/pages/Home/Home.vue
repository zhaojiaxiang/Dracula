<template>
    <div class="body-color" style="margin-right:30px">
        <Guide>
            <template>
                <div><h5><strong>我参与的项目</strong></h5></div>
            </template>
        </Guide>
        <ProjectItem ref="ProjectItem"></ProjectItem>
        <Guide>
            <template>
                <div><h5><strong>我参与的任务</strong></h5></div>
            </template>
        </Guide>
        <SlipNoNew @click="openSlipNoNew()" @refreshHome="refreshHome"></SlipNoNew>
        <SlipNoModify @click="openSlipNoModifiy(val)" @refreshHome="refreshHome"></SlipNoModify>
        <SlipNoItem ref="SlipNoItem" @refreshHome="refreshHome"></SlipNoItem>
    </div>
</template>

<script>
import Guide from './components/Guide'
import ProjectItem from './components/ProjectItem'
import SlipNoItem from './components/SlipNoItem'
import SlipNoNew from './components/SlipNoNew'
import SlipNoModify from './components/SlipNoModify'
export default {
    name: "Home",
    components:{
        Guide,
        ProjectItem,
        SlipNoItem,
        SlipNoNew,
        SlipNoModify
    },
    methods:{
        refreshHome(){
            this.$refs.ProjectItem.refreshProjectItems()
            this.$refs.SlipNoItem.refreshLiaisons()
        }
    }
}
</script>

<style scoped>
</style>
