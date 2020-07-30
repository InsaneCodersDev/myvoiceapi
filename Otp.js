const mongoose = require('mongoose');

const otpSchema = new mongoose.Schema({
    "username":{
        type:String,
        required:true
    },
    "otp":{
        type:Number,
        required:true
    }
});

const OTP = mongoose.model('employ_otp',otpSchema);
module.exports = OTP;