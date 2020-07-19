const mongoose = require('mongoose');

const exceptionSchema = new mongoose.Schema({
"username":{
    type:String,
    required:true
},
"name":{
    type:String,
    required:true
},
"subject":{
    type:String,
    required:true
},
"message":{
    type:String,
    required:true
},
"proof":{
    type:String,
    required:true
}
});

const Exception = mongoose.model('Employ_exception',exceptionSchema);
module.exports = Exception;