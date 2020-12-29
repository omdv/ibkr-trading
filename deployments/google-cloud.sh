#!/bin/sh
gcloud compute instances create ibkr \
--zone=us-central1-f \
--machine-type=e2-small \
--image-family=cos-stable \
--image-project=cos-cloud \
--tags=http-server,https-server \
--boot-disk-size=10GB