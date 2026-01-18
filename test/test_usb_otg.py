import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32s2", "esp32s3", "esp32p4"])
def test_usb_serial_jtag(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/examples/peripherals/usb/device/tusb_console/firmware.uf2",
            "--timeout",
            "8000",
            "--expect-text",
            ") example: log -> USB",
            "--diagram-file",
            f"usb_otg/diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
