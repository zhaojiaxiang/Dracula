<template>
    <div>
        <el-dialog :title="title" :visible.sync="dialogEdit" width="40%" :before-close="handleClose"
            :show-close="false">
            <el-form ref="form" :model="form" label-position="right" label-width="80px">
                <el-form-item prop="fsystem" label="系统">
                    <el-select class="input-short" v-model="form.fsystem" :disabled="!newflg" clearable>
                        <el-option v-for="item in systemList" :key="item.value" :label="item.value" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item prop="fcomment" label="程序">
                    <el-input class="input-short" v-model="form.fcomment" :disabled="!newflg" clearable></el-input>
                </el-form-item>
                <el-form-item prop="fslipno" label="联络票号">
                    <el-input class="input-short" v-model="form.fslipno" :disabled="!newflg" clearable></el-input>
                </el-form-item>
                <el-form-item prop="fchkoutobj" label="迁出文件">
                    <el-input class="input-long" v-model="form.fchkoutobj" :disabled="!newflg" clearable></el-input>
                </el-form-item>
                <el-form-item prop="fchkoutfile" label="迁出PBL" v-if="!newflg">
                    <el-input class="input-long" v-model="form.fchkoutfile" clearable></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogEdit = false">取 消</el-button>
                <el-button @click="resetInput('form')" v-if="newflg">重 置</el-button>
                <el-button v-if="newflg" @click="updateContinue('form')">继续新建</el-button>
                <el-button type="primary" @click="updateCheckout('form')">{{this.btntext}}</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import {
        getCheckoutData,
        updateCheckoutData,
        newCheckoutData,
    } from "../../../services/checkoutService";

    export default {
        data() {
            return {
                title: "",
                dialogEdit: false,
                id: "",
                btntext: "",
                newflg: true,
                form: {
                    fsystem: '',
                    fcomment: '',
                    fslipno: '',
                    fchkoutobj: '',
                    fchkoutfile: '',
                    fchkstatus: '',
                },
                systemList: [{
                        value: "OMS",
                        label: "OMS",
                    },
                    {
                        value: "OMR",
                        label: "OMR",
                    },
                    {
                        value: "OMZ",
                        label: "OMZ",
                    },
                    {
                        value: "OMB",
                        label: "OMB",
                    },
                    {
                        value: "OMI",
                        label: "OMI",
                    },
                    {
                        value: "OMIIAB",
                        label: "OMIIAB",
                    },
                    {
                        value: "GCS",
                        label: "GCS",
                    },
                ],
            };
        },

        methods: {
            async init(model, id) {
                this.resetInput('form');
                if (model === 'new') {
                    this.title = "新建";
                    this.btntext = "新 建";
                    this.newflg = true;
                } else {
                    this.title = "修改";
                    this.btntext = "修 改";
                    this.newflg = false;
                    this.id = id;
                    var resp = await getCheckoutData(id);
                    this.form = resp.data;
                }
                this.dialogEdit = true;
            },

            resetInput(formname) {
                if (this.$refs[formname] !== undefined) {
                    this.$refs[formname].resetFields();
                }
            },

            async updateCheckout(formname) {
                this.$refs[formname].validate(async (valid) => {
                    if (valid) {
                        if (this.newflg) {
                            this.form.fchkstatus = '1-ASK';
                            var respnew = await newCheckoutData(this.form);
                            if (respnew.status === 201) {
                                this.$emit("refreshCheckoutList");
                                this.dialogEdit = false;
                                this.$message({
                                    message: "CheckOut记录新建成功",
                                    type: "success",
                                })
                            } else {
                                this.$message({
                                    message: respnew.data.message,
                                    type: "error",
                                })
                            }
                        } else {
                            if (this.form.fchkoutfile !== '') {
                                this.form.fchkstatus = '2-Check Out';
                            }
                            var respmodify = await updateCheckoutData(this.id, this.form);
                            if (respmodify.status === 200) {
                                this.$emit("refreshCheckoutList");
                                this.dialogEdit = false;
                                this.$message({
                                    message: "CheckOut记录更新成功",
                                    type: "success",
                                })
                            } else {
                                this.$message({
                                    message: respnew.data.message,
                                    type: "error",
                                })
                            }
                        }
                    }
                });
            },

            async updateContinue(formname) {
                this.$refs[formname].validate(async (valid) => {
                    if (valid) {
                        this.form.fchkstatus = '1-ASK';
                        var respnew = await newCheckoutData(this.form);
                        if (respnew.status === 201) {
                            this.$emit("refreshCheckoutList");
                            this.$message({
                                message: "CheckOut记录新建成功",
                                type: "success",
                            });
                            this.form.fchkoutobj = '';
                        } else {
                            this.$message({
                                message: respnew.data.message,
                                type: "error",
                            })
                        }
                    }
                })
            },

            handleClose() {
                //不关闭
                return false;
            }
        },
    };
</script>
<style scoped>
    .input-short {
        width: 40%;
    }

    .input-long {
        width: 70%;
    }
</style>
