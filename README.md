# rAIdio

## Abstract

This project aims to use the latest developments in generative artificial intelligence to create an advanced system that mimics internet radio. The project integrates state-of-the-art technologies in text generation, music generation, and human voice synthesis to create a cohesive system. The solution not only enables playback of artificially generated broadcasts but also opens up a whole new dimension of exploring musical genres and styles.

## How to run

To run project you need to install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

Then you need to run the following command:
```docker compose up --build```

## How to use

After running project you can access client app on [localhost:3000](http://localhost:5000/).

## Project structure

Project is divided into 4 main parts:

- [player](./player) - React app that is the frontend client of the project
- [radio](./radio) - Python projet that generates radio content
- [golang-server-live](./golang-server-live) - Golang server that streams generated content
- [scheduler](./scheduler) - Simple container with cron job that triggers content generation

In the [channels](./channels) folder you can find all the generated content for each channel.

[radio_config.json](./radio_config.json) file contains configuration for the radio.

## Demo

You can see demo files for this project in [demo_files](./demo_files) folder.
It contains:

- Video materials showcasing the project
- Sample radio content for each channel: broadcast, generated music, generated speaker voice
