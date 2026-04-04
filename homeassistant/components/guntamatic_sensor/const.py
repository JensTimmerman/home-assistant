"""Constants for the guntamatic integration."""

from datetime import timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

DOMAIN = "guntamatic_sensor"
SCAN_INTERVAL = timedelta(seconds=30)
DIAGNOSTIC_SENSORS = {"Serial", "Version", "Operat. time", "Service Hrs"}


SENSOR_DEVICE_CLASSES: dict[str, SensorDeviceClass | None] = {
    "Boiler temperature": SensorDeviceClass.TEMPERATURE,
    "Outside Temp.": SensorDeviceClass.TEMPERATURE,
    "Buffer Top": SensorDeviceClass.TEMPERATURE,
    "Buffer Mid": SensorDeviceClass.TEMPERATURE,
    "Buffer Btm": SensorDeviceClass.TEMPERATURE,
    "DHW 0": SensorDeviceClass.TEMPERATURE,
    "DHW 1": SensorDeviceClass.TEMPERATURE,
    "DHW 2": SensorDeviceClass.TEMPERATURE,
    "CO2 Content": SensorDeviceClass.CO2,
    "Operat. time": SensorDeviceClass.DURATION,
}

SENSOR_STATE_CLASSES: dict[str, SensorStateClass | None] = {
    "Boiler temperature": SensorStateClass.MEASUREMENT,
    "Outside Temp.": SensorStateClass.MEASUREMENT,
    "Buffer load.": SensorStateClass.MEASUREMENT,
    "CO2 Content": SensorStateClass.MEASUREMENT,
}
