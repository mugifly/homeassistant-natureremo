"""Nature Remo as Sensor"""

# Import the device class
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

# Import constants
# https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/const.py
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_SCAN_INTERVAL, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS

# Import classes for validation
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Import class for interval check
import time

# Import the logger for debugging
import logging

# Define the required pypi package
REQUIREMENTS = ['pyture-remo==0.2']

# Define the validation of configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
})

# Initialize the logger
_LOGGER = logging.getLogger(__name__)

# Remo API Update Interval (msec.)
REMO_API_UPDATE_INTERVAL = 60000


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup platform."""

    access_token = config[CONF_ACCESS_TOKEN]

    import pyture_remo
    remo = pyture_remo.Remo(access_token)

    # Add sensors on Remo to Home Assistant as device
    _LOGGER.debug('Finding Nature Remo...')
    sensor_devices = []

    for remo_device in remo.find_devices():

        _LOGGER.debug('Nature Remo detected...' + remo_device.name)

        # Add temparature sensor
        sensor_devices.append(NatureRemoSensor(remo, remo_device, DEVICE_CLASS_TEMPERATURE))

        # Add humidity sensor
        sensor_devices.append(NatureRemoSensor(remo, remo_device, DEVICE_CLASS_HUMIDITY))

    add_devices(sensor_devices)


class NatureRemoSensor(Entity):

    def __init__(self, remo_client, remo_device, sensor_class) -> None:
        """Initialzing sensor of Nature Remo...."""

        # Initialize a state of this sensor
        self._state = None

        # Set an API client of Remo for state updating
        self._remo_client = remo_client

        # Set an object of this sensor
        self._remo_device = remo_device
        self._sensor_class = sensor_class;
        self._updated_at = 0

        # Set a name of this sensor
        if self._sensor_class == DEVICE_CLASS_TEMPERATURE:
            self._name = self._remo_device.name + ' Temperature'
        elif self._sensor_class == DEVICE_CLASS_HUMIDITY:
            self._name = self._remo_device.name + ' Humidity'
        else:
            self._name = self._remo_device.name

    @property
    def name(self) -> str:
        """Return the name of this sensor."""
        return self._name

    @property
    def state(self) -> str:
        """Return the state of this sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""

        if self._sensor_class == DEVICE_CLASS_TEMPERATURE:
            return TEMP_CELSIUS

        elif self._sensor_class == DEVICE_CLASS_HUMIDITY:
            return '%'

    @property
    def device_state_attributes(self) -> str:
        """Return the attributes of this sensor."""
        return {
            "remo_device_id": self._remo_device.id,
            "remo_device_name": self._remo_device.name,
            "remo_firmware_version": self._remo_device.firmware_version,
            "remo_temperature_offset": self._remo_device.temperature_offset,
            "remo_humidity_offset": self._remo_device.humidity_offset
        }

    @property
    def unique_id(self) -> str:
        """Return a unique identifier for this device."""
        return 'remo_device_' + self._remo_device.id + '_' + self._sensor_class

    def update(self) -> None:
        """Fetch new state data for the sensor."""

        # Check interval
        if (time.time() - self._updated_at) < REMO_API_UPDATE_INTERVAL:
            return

        # Update device information
        _LOGGER.info('Updating sensor data...' + self._remo_device.name)
        self._remo_device = self._remo_client.find_device(self._remo_device.name)
        self._updated_at = time.time()

        # Get a state
        if self._sensor_class == DEVICE_CLASS_TEMPERATURE:
            self._state = str(round(self._remo_device.get_temperature(), 1))

        elif self._sensor_class == DEVICE_CLASS_HUMIDITY:
            self._state = self._remo_device.get_humidity()
