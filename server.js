const express = require("express");
const app = express();
const queue = require("queue");
const bodyParser = require("body-parser");
const expressWs = require("express-ws")(app);

const q = queue({ autostart: true });
const messages = [];

app.use(bodyParser.json());

app.post("/webhook", function(req, res, next) {
  data = JSON.stringify(req.data)
  q.push(cb => {
    messages.push(data);
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
    ws.send(messages.pop());
  });
});

app.listen(3000);
