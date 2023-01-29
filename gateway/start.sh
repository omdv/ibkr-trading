#!/bin/bash
set -e

echo "Starting Xvfb..."
/usr/bin/xvfb-run --auto-servernum /opt/ibc/gatewaystart.sh -inline &

echo "Setup port forwarding..."
socat TCP-LISTEN:4041,fork TCP:localhost:4001,forever &
socat TCP-LISTEN:4042,fork TCP:localhost:4002,forever &

echo "IB gateway is ready."
