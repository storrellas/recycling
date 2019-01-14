import os

MQTT = {
    'hostname': os.environ.get('MOSQUITTO_HOST'),
    'topic_sensor_detection': 'sec2sky/detection',
    'topic_sensor_register': 'sec2sky/register',
    'topic_sensor_status': 'sec2sky/status'
}
print(MQTT)
