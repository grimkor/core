"""Turn the switch on."""
from typing import Any, Dict

from surepy import SureProductID

from homeassistant.components.switch import SwitchDevice
from homeassistant.const import CONF_ID, CONF_TYPE

from .const import DATA_SURE_PETCARE, SPC

"""Turn the switch on."""


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Turn the switch on."""
    spc = hass.data[DATA_SURE_PETCARE][SPC]

    pets = [MySwitch(id, spc) for id in spc.ids if id[CONF_TYPE] == SureProductID.PET]
    async_add_entities(pets, True)


"""Turn the switch on."""


class MySwitch(SwitchDevice):
    """Turn the switch on."""

    def __init__(self, id, spc):
        """Turn the switch on."""
        self._id = id[CONF_ID]
        self._name = f"spc-{id[CONF_ID]}-switch"
        self._spc = spc
        self._spc_data: Dict[str, Any] = self._spc.states[SureProductID.PET].get(
            self._id
        )
        print(self._spc_data["position"]["where"])
        self._is_on = self._spc_data["position"]["where"] == 1

    """Turn the switch on."""

    @property
    def unique_id(self):
        """Turn the switch on."""
        return self._name

    @property
    def name(self):
        """Turn the switch on."""
        return self._spc_data["name"]

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False

    async def async_update(self) -> None:
        """Get the latest data and update the state."""
        self._spc_data: Dict[str, Any] = self._spc.states[SureProductID.PET].get(
            self._id
        )
        self._is_on = self._spc_data["position"]["where"] == 1
