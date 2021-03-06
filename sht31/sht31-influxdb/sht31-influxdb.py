from sht31 import sht31
from influxdb import InfluxDBClient
import socket
import time

# Set the bus number and device address
mysht31 = sht31.SHT31(0, 0x44)

hostname = socket.gethostname()

client = InfluxDBClient(host='influxdb', port=8086)
client.create_database('sht31')
client.switch_database('sht31')

data = [
    {
        "measurement": "conditions",
        "tags": {
            "host": "",
        },
        "fields": {
            "cTemp": "",
            "fTemp": "",
            "humidity": "",
        }
    }
]

while True:
    # Read data from the sensor
    sensor_data = mysht31.read_sht31()

    # Process data
    cTemp, fTemp, humidity = mysht31.process_data(sensor_data)

    data[0]["fields"]["cTemp"] = cTemp
    data[0]["fields"]["fTemp"] = fTemp
    data[0]["fields"]["humidity"] = humidity
    data[0]["tags"]["host"] = hostname

    client.write_points(data)
    time.sleep(3)
