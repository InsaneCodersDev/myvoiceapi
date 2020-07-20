var express = require("express");
var fs = require("fs");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
var app = express();
const db = require("./user");
const Exception = require("./Exceptions");
var multer = require("multer");
var path = require('path');
// Storage Strategy
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname+"../../VoidAdmin/uploads/"));
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });
//connect to mongodb
mongoose.connect(
  "mongodb+srv://ovi:ovi@cluster0-ivsyl.mongodb.net/Attendnace?retryWrites=true&w=majority",
  { useNewUrlParser: true, useUnifiedTopology: true }
);

mongoose.connection
  .once("open", function () {
    console.log("Connection has been made, Now make fireworks");
  })
  .on("error", function (error) {
    console.log("Connection Error:", error);
  });

mongoose.Promise = global.Promise;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

function runScript() {
  return spawn("python3", ["-u", path.join(__dirname, "recognize.py"), A]);
}

function runScriptAddUser(name) {
  return spawn("python3", ["-u", path.join(__dirname, "add_user.py"), name]);
}

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "*");
  if (req.method === "OPTIONS") {
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET");
    return res.status(200).json({});
  }
  next();
});

app.get("/db/:username", function (req, res) {
  db.findOne({ username: req.params.username }).then((user) => {
    res.send(user);
  });
});

app.get("/db/email/:email", function (req, res) {
  db.findOne({ email: req.params.email }).then((email) => {
    res.send(email);
  });
});

app.get("/photo/:username", function (req, res) {
  db.findOne({ username: req.params.username }).then((user) => {
var x = path.join(__dirname+"../../VoidAdmin/img/");
    res.sendFile(x + user.image_url);
console.log(x);
  });
});

app.post("/db/exception/add", upload.single("exceptionfile"), function (
  req,
  res
) {
  console.log(req.file);
  console.log(req.body);
  const exception = new Exception({
    username: req.body.username,
    name: req.body.name,
    subject: req.body.subject,
    message: req.body.message,
    proof: req.file.originalname,
  });
  exception.save().then(() => {
    console.log("Upload Hogaya");
    res.send("Form Submitted");
  });
});

var A;

app.post("/api", function (req, res) {
  A = Date.now() + ".wav";
  console.log(A);
  var myFile = fs.createWriteStream(A);
  console.log("rcvd post request");
  req.pipe(myFile);
  const subprocess = runScript();
  subprocess.stdout.on("data", (data) => {
    console.log(`data:${data}`);
    var name = `${data}`;
    res.send(name);
  });
  subprocess.stderr.on("data", (data) => {
    console.log(`error:${data}`);
  });
  subprocess.on("close", () => {
    console.log("Closed");
  });
});

app.post("/upload/:id/:name", function (req, res) {
  console.log("rcvd post request");
  console.log(req.params.id);
  const source = "./voice_database/" + req.params.name.toString();
  fs.mkdir(source, (e) => {
    console.log(e);
  });
  var myFile = fs.createWriteStream(
    source + "/" + req.params.id.toString() + ".wav"
  );
  req.pipe(myFile);
  res.send("New User " + req.params.name + " Added");
});

app.get("/adduser/:name", function (req, res) {
  console.log(req.body);
  const subprocess = runScriptAddUser(req.params.name);
  console.log("got " + req.params.name);
  subprocess.stdout.on("data", (data) => {
    console.log(`data:${data}`);
    var name = `${data}`;
    res.send(name);
  });
  subprocess.stderr.on("data", (data) => {
    console.log(`error:${data}`);
  });
  subprocess.on("close", () => {
    console.log("Closed");
  });
});

app.listen(5000);
