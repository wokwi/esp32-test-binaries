import os
import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c5", "esp32c6", "esp32c61", "esp32s31"])
def test_wifi_function(chip: str):

    # Prefer the per-test diagram override (it raises cpuFrequency so the suite
    # fits into the scenario timeout), and fall back to the shared board diagram.
    diagram_file = f"wifi_function/diagram.{chip}.json"
    if not os.path.exists(diagram_file):
        diagram_file = f"diagram.{chip}.json"

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
            diagram_file,
        ]
    )
    assert result.returncode == 0
