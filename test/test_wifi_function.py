import os
import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6"])
def test_wifi_function(chip: str):

    diagram_dir = "wifi_function/" if chip == "esp32c6" else ""

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_wifi/test_apps/wifi_function/firmware.uf2",
            "--timeout",
            "5000",
            "--scenario",
            "test_wifi_function.scenario.yaml",
            "--diagram-file",
            f"{diagram_dir}diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
