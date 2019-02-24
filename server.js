const express = require("express");
const app = express();
const queue = require("queue");
const bodyParser = require("body-parser");
const expressWs = require("express-ws")(app);

const q = queue({ autostart: true });
const messages = [];

app.use(bodyParser.json());

app.post("/", function(req, res, next) {
  console.log("post route", req.testing);
  q.push(cb => {
    messages.push(req.body);
    cb();
  });
  res.end();
});

app.ws("/", function(ws, req) {
  const apiKey = req.query.apiKey;

  if (!apiKey || apiKey != process.env.API_KEY) {
    ws.close();
  }

  ws.on("message", function(msg) {
    console.log(msg);
  });

  q.on("success", function(result, job) {
    console.log(result, job);
    ws.send(JSON.stringify(messages.pop()));
  });
});

app.listen(3000);
