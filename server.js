const express = require("express");
const https = require("https");
const fs = require("fs");
const app = express();
const queue = require("queue");
const bodyParser = require("body-parser");

const q = queue({ autostart: true });
const messages = [];

const { CERTIFICATE_PATH, PRIVATE_KEY_PATH, API_KEY } = process.env;

const privateKey = fs.readFileSync(PRIVATE_KEY_PATH);
const certificate = fs.readFileSync(CERTIFICATE_PATH);

const httpsServer = https.createServer(
  {
    key: privateKey,
    cert: certificate
  },
  app
);
const expressWss = require("express-ws")(app, httpsServer);

app.use(bodyParser.json());

app.post("/webhook", function(req, res, next) {
  data = JSON.stringify(req.data);
  q.push(cb => {
    messages.push(data);
    cb();
  });
  res.send(200);
});

app.ws("/", function(ws, req) {
  const apiKey = req.query.apiKey;

  if (!apiKey || apiKey != API_KEY) {
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

httpsServer.listen(3000);
