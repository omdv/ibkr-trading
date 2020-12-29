socat TCP-LISTEN:4041,fork TCP:localhost:4001,forever &
socat TCP-LISTEN:4042,fork TCP:localhost:4002,forever &

/opt/ibc/gatewaystart.sh -inline &