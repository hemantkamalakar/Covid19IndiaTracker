"""
A platform which allows you to get information about Corona status in India.
For more details about this component, please refer to the documentation at
https://github.com/custom-components/Covid19IndiaTracker
"""
# pylint: disable=unused-argument,missing-docstring
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from integrationhelper import WebClient, Logger
from integrationhelper.const import CC_STARTUP

URL = "https://api.covid19india.org/data.json"
ISSUE_LINK = "https://github.com/custom-components/Covid19IndiaTracker/issues/"
SCAN_INTERVAL = timedelta(seconds=120)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    logger = Logger(__name__)
    logger.info(CC_STARTUP.format(name="Covid19IndiaTracker", issue_link=ISSUE_LINK))
    webclient = WebClient(async_get_clientsession(hass), logger)
    async_add_entities([Covid19IndiaTrackerSensor(webclient)], True)


class Covid19IndiaTrackerSensor(Entity):
    def __init__(self, webclient):
        self._state = None
        self._confirmed = None
        self._maharashtra_confirmed = None
        self._totaldeaths = None
        self.webclient = webclient

    async def async_update(self):
        Covid19IndiaTracker = await self.webclient.async_get_json(
            URL, {"Accept": "application/json"}
        )
        rbd = Covid19IndiaTracker[0]
        self._state = rbd.statewise[0].confirmed #rbd["tagline"]
        self._confirmed = rbd.statewise[0].confirmed #rbd["tagline"]
        self._maharashtra_confirmed = rbd.statewise[1].confirmed #rbd["tagline"]
        self._totaldeaths = rbd.statewise[0].deaths

    @property
    def name(self):
        return "INDIA COVID-19 TRACKER"

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi-emoticon-devil"

    @property
    def device_state_attributes(self):
        return {"Confirmed cases": self._confirmed, "Deaths": self._totaldeaths}
