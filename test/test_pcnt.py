import os
import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_pcnt(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_pcnt/test_apps/pulse_cnt/firmware.uf2",
            "--timeout",
            "5000",
            "--scenario",
            "test_pcnt.scenario.yaml",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
