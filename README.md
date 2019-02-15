# Build Status Lights

This is a Python server that uses Bitbucket Webhooks to display project build statuses on a [Nanoleaf](https://nanoleaf.me/) light panel.

## Getting Started

Right now, in order to use this server you need to be using Bitbucket build pipelines and have a Nanoleaf light panel (Aurora or Canvas) setup on your local network.

Clone this repository

```
git clone https://github.com/astone123/build-status-lights.git
```

Configure the server by replacing example configuration values with your actual information

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

## Run with Docker

`docker build -t build-status-lights .`

`docker run -d -p 8000:8000 build-status-lights`

## Exposing your Server

You'll need to either adjust your router settings or use a program like [ngrok](https://ngrok.com/) to expose port 8000 on your server so that Bitbucket can send requests to it.

## Set up Bitbucket Webhooks

Go to each Bitbucket project that you put in your `config.yaml` file, navigate to `Settings > Webhooks > Add Webhook`.

Enter the URL for your server, and under `Triggers`, select `Choose from a list of triggers` and check `Build status created` and `Build status updated`.
