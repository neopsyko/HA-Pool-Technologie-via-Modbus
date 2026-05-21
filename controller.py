import logging
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
_PROBE_INTERVAL = 5  # une tentative de reconnexion toutes les N itérations échouées

class PoolController:
    def __init__(self, hass, update_callback, scan_interval, handler):
        self._hass = hass
        self._update_callback = update_callback
        self._scan_interval = scan_interval
        self._remove_listener = None
        self._handler = handler
        self.modbus_ok = False
        self._modbus_fail_count = 0
        self._modbus_fail_threshold = 5
        self._probe_counter = 0

    @property
    def scan_interval(self):
        return self._scan_interval

    @property
    def handler(self):
        return self._handler

    async def start(self):
        self._start_polling()

    def _start_polling(self):
        if self._remove_listener:
            self._remove_listener()
        self._remove_listener = async_track_time_interval(
            self._hass, self._update_callback, timedelta(seconds=self._scan_interval)
        )

    async def update_interval(self, new_interval):
        self._scan_interval = new_interval
        self._start_polling()

    def notify_modbus_success(self):
        self._modbus_fail_count = 0
        self._probe_counter = 0
        self.modbus_ok = True

    def notify_modbus_failure(self):
        self._modbus_fail_count += 1
        if self._modbus_fail_count >= self._modbus_fail_threshold:
            self.modbus_ok = False

    def should_skip_poll(self) -> bool:
        """Retourne True si le poll doit être sauté (Modbus déconnecté).

        Autorise une tentative de reconnexion toutes les _PROBE_INTERVAL itérations.
        """
        if self._modbus_fail_count < self._modbus_fail_threshold:
            return False
        self._probe_counter += 1
        if self._probe_counter >= _PROBE_INTERVAL:
            self._probe_counter = 0
            _LOGGER.debug("Modbus déconnecté — tentative de reconnexion")
            return False
        _LOGGER.debug(
            "Modbus déconnecté — poll ignoré (%d/%d avant nouvelle tentative)",
            self._probe_counter,
            _PROBE_INTERVAL,
        )
        return True
