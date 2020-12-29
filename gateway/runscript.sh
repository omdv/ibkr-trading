socat TCP-LISTEN:4000,fork TCP:localhost:4002,forever &

/opt/ibc/gatewaystart.sh -inline &