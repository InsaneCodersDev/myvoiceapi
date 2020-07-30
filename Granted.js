const mongoose = require('mongoose');

const grantedSchema = new mongoose.Schema({
"username":{
    type:String,
    required:true
},
"duration":{
    type:Date,
    required:true
},
"type":{
    type:String,
    required:true
},
"days":{
    type:Number
},
"status":{
    type:Boolean,
    required:true
}
});

const Exception = mongoose.model('Employ_grant',grantedSchema);
module.exports = Exception;