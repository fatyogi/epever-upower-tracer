from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "solar"
ifdb   = "solar"
ifhost = "127.0.0.1"
ifport = 8086

# device configuration
SDM_PORT="/dev/ttyXRUSB0"
TRACER_PORT="/dev/ttyXRUSB1"
