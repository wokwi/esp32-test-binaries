import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_usb_serial_jtag(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_usb_serial_jtag/test_apps/usb_serial_jtag/firmware.uf2",
            "--timeout",
            "30000",
            "--scenario",
            "test_usb_serial_jtag.scenario.yaml",
            "--diagram-file",
            f"usb_serial_jtag/diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
