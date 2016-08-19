# GoTryGo - ![CircleCI](https://circleci.com/gh/Spark-Networks/gotrygo.svg?style=shield&circle-token=:circle-token)

A simple Go app for testing builds/deployments in docker.

To build locally (must have go installed), run:

    go get
    make build

This will create an unversioned static linux binary `gotrygo` You can then run `docker build .` to create a base ("scratch") docker container configured to run the app on startup.

If desired, `circle.yml` contains all these steps wrapped into a single CircleCI build. The docker image is uploaded to Docker Hub under the name "sparknetworks/gotrygo" and tagged with the same tag as was passed in by git. That same tag is baked into the go binary at build time as well. At the moment, ONLY tags are being built, all other requests should be ignored.

We have also added a python script for testing the application once running on the docker cluster, showing the number of requests being served by the various containers and if there are any dropped/bad requests. Basic usage is:

    python gotrygo_test.py < url_to_application >

The current deployed location of the test cluster is http://elb-1312002678.us-west-1.elb.amazonaws.com/
