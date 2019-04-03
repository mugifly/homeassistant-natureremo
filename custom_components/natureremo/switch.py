"""Nature Remo as Switch"""

# Import the device class
from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA

# Import constants
# https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/const.py
from homeassistant.const import CONF_ACCESS_TOKEN

# Import classes for validation
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

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


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup platform."""

    access_token = config[CONF_ACCESS_TOKEN]

    import pyture_remo
    remo = pyture_remo.Remo(access_token)

    # Add appliances on Remo to Home Assistant as device
    _LOGGER.debug('Finding appliances on Nature Remo...')
    add_devices(NatureRemoSwitch(appliance) for appliance in remo.find_appliances())


class NatureRemoSwitch(SwitchDevice):

    def __init__(self, appliance) -> None:
        """Initialzing appliance of Nature Remo...."""

        # Initialize a state of this appliance
        self._state = None

        # Set an object of this appliance
        self._appliance = appliance
        self._name = appliance.nickname

        _LOGGER.info('Appliance detected... ' + self._name)

    @property
    def name(self) -> str:
        """Return the name of this appliance."""
        return self._name

    @property
    def device_state_attributes(self) -> str:
        """Return the attributes of this appliance."""
        return {
            "friendly_name": self._appliance.nickname,
            "appliance_id": self._appliance.id,
            "appliance_nickname": self._appliance.nickname,
            "appliance_image": self._appliance.image,
            "appliance_type": self._appliance.type
        }

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return self._state

    @property
    def assumed_state(self) -> bool:
        """Use the assumed state because we can't get the actual status of the device via Remo."""
        return True

    @property
    def unique_id(self) -> str:
        """Return a unique identifier for this device."""
        return 'remo_' + self._appliance.type + '_' + self._appliance.id

    def turn_on(self, **kwargs) -> None:
        """Turn on device via Remo."""

        # Find the signal to turn on the power of this appliance
        _LOGGER.info('Finding signals...')
        all_signals = self._appliance.find_signals()
        _LOGGER.info('Found signals...' + str(len(all_signals)))
        turn_on_signal = None

        for signal in all_signals:
            if signal.image == 'ico_on': # Turn on the power
                turn_on_signal = signal
                break

        if turn_on_signal == None:
            for signal in all_signals:
                if signal.image == 'ico_io': # Toggle the power
                    turn_on_signal = signal
                    break

        if turn_on_signal == None:
            _LOGGER.error('Could not find a signal to turn on the power for ' + self._name)
            return

        # Send the signal
        turn_on_signal.send()

        # Change the state on Home Assistant
        self._state = True

    def turn_off(self, **kwargs) -> None:
        """Turn on device via Remo."""

        # Find the signal to turn off the power of this appliance
        _LOGGER.info('Finding signals...')
        all_signals = self._appliance.find_signals()
        _LOGGER.info('Found signals...' + str(len(all_signals)))
        turn_off_signal = None

        for signal in all_signals:
            if signal.image == 'ico_off': # Turn off the power
                turn_off_signal = signal
                break

        if turn_off_signal == None:
            for signal in all_signals:
                if signal.image == 'ico_io': # Toggle the power
                    turn_off_signal = signal
                    break

        if turn_off_signal == None:
            _LOGGER.error('Could not find a signal to turn off the power for ' + self._name)
            return

        # Send the signal
        turn_off_signal.send()

        # Change the state on Home Assistant
        self._state = False
