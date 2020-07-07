const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
  department: {
    type: String,
    required: true,
  },
  dob: {
    type: Date,
    required: true,
  },
  designation: {
    type: String,
    required: true,
  },
  username: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  image_url: {
    type: String,
    required: true,
  },
});

const Users = mongoose.model("Employ_registration", userSchema);
module.exports = Users;
