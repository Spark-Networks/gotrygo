# GoTryGo

A simple Go app for testing builds/deployments in docker.

To build locally (must have go installed), run:

    go get
    make build

This will create a static linux binary `gotrygo` You can then run `docker build .` to create a base ("scratch") docker container configured to run the app on startup.

If desired, `circle.yml` contains all these steps wrapped into a single CircleCI build. It currently creates the docker images as an artifact that can be loaded directly into your docker engine. In the future, this should be updated to instead upload the image to a docker registry for easier use.
