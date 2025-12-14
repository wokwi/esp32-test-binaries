import os
import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32", "esp32s2", "esp32s3", "esp32c5", "esp32p4"])
def test_psram(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_psram/test_apps/psram/firmware.uf2",
            "--timeout",
            "60000",
            "--scenario",
            "test_psram.scenario.yaml",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
