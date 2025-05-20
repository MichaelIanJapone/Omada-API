from influxdb_client import InfluxDBClient, WritePrecision, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG

def get_influx_client():
    return InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)

def write_points(write_api, bucket, org, points):
    write_api.write(bucket=bucket, org=org, record=points)
