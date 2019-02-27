# Build Status Lights

This is a Python websocket client that receives Bitbucket webhook data from a websocket server to display project build statuses on a [Nanoleaf](https://nanoleaf.me/) light panel.

## Getting Started

Right now, in order to use this client you need a websocket server that is receiving Bitbucket webhook data and forwarding it to websocket clients, and have a Nanoleaf light panel (Aurora or Canvas) setup on your local network. You can use [simple-websocket-server](https://github.com/astone123/simple-websocket-server.git) to forward webhook data to this client.

Clone this repository

```
git clone https://github.com/astone123/build-status-lights.git
```

Configure the client by replacing example configuration values with your actual information

```
cp config.example.yaml config.yaml
```

Configuration values:

- `projects`
  - This is a list of the projects that you want to monitor with the lights. Each project needs to have a `repo_url` and `branch`. The project can optionally include a list of `tile_ids` to specify the Nanoleaf tiles to be associated with the project.
- `nanoleaf`
  - `ip`
    - This is the IP address of your Nanoleaf light panels on your local network
  - `authorization_token`
    - This is the auth token used to communicate with your Nanoleaf light panels. You can obtain one of these by holding the power button on your light panel controls for 5-7 seconds and then sending this request to your lights
      ```
      curl -X POST "http://<your-light-panel-ip-address>:16021/api/v1/new"
      ```
- `colors`
  - These are the colors that will display for each build status.
- `api_key` (optional)
  - This is an api key that will be sent with the webhook client's connection request
- `ws_server_hostname`
  - The hostname where your websocket server is running
- `ws_server_port`
  - The port that your websocket server is running on

After your client is configured, run

```
python ws_client.py
```

the websocket client should then connect to your server and be ready to receive webhook data.
