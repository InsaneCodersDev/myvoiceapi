const mongoose = require('mongoose');

const attendanceSchema = new mongoose.Schema({
    "username":{
        type:String,
        required:true
    },
    "date":{
        type:Number,
        required:true
    },
    "month":{
        type:Number,
        required:true
    },
    "year":{
        type:Number,
        required:true
    },
    "time":{
        type:String,
        required:true
    },
    "interface":{
        type:String,
        required:true
    },
    "attendance":{
        type:Boolean,
        required:true
    }
});

const Attendance = mongoose.model('Employ_attendance_login',attendanceSchema);
module.exports = Attendance;