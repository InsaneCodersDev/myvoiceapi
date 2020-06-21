var express = require('express');
var fs = require('fs');

const path = require('path');
const { spawn } = require('child_process');
var app = express();

function runScript(){
    return spawn('python3',[
        "-u",
        path.join(__dirname, 'recognize.py'),
    ]);
}

function runScriptAddUser(name){
    return spawn('python3',[
        "-u",
        path.join(__dirname, 'add_user.py'),
        name
    ]);
}


app.use((req, res, next)=>{
    res.header('Access-Control-Allow-Origin','*');
    res.header('Access-Control-Allow-Headers','*');
    if(req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Methods','PUT,POST,GET');
        return res.status(200).json({});
    }
    next();
})


app.post('/api', function(req, res){
    var myFile = fs.createWriteStream("myoutput.wav");
    console.log('rcvd post request');
    req.pipe(myFile);
    const subprocess = runScript();
    subprocess.stdout.on('data', (data) => {
        console.log(`data:${data}`);
        var name = `${data}`;
        res.send(name);
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`error:${data}`);
    });
    subprocess.on('close', () => {
        console.log("Closed");
    });
});

app.post('/upload/:id/:name', function(req, res){
    console.log('rcvd post request');
    console.log(req.params.id);
    const source = "./voice_database/" + req.params.name.toString();
    fs.mkdir(source,(e)=>{
        console.log(e);
    });
    var myFile = fs.createWriteStream(source+'/'+req.params.id.toString()+'.wav');
    req.pipe(myFile);
    res.send('New User ' +req.params.name+ ' Added');
});

app.get('/adduser/:name',function(req,res){
    console.log(req.body);
    const subprocess = runScriptAddUser(req.params.name);
    console.log('got '+req.params.name);
    subprocess.stdout.on('data', (data) => {
        console.log(`data:${data}`);
        var name = `${data}`;
        res.send(name);
    });
    subprocess.stderr.on('data', (data) => {
        console.log(`error:${data}`);
    });
    subprocess.on('close', () => {
        console.log("Closed");
    });

});

app.listen(5000);
