import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32p4"])
def test_wifi_function(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/examples/wifi/getting_started/station/firmware.uf2",
            "--timeout",
            "8000",
            "--expect-text",
            "wifi station: connected to ap SSID:Wokwi-GUEST password:",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
