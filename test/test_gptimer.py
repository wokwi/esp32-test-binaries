import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c5", "esp32c6", "esp32h2"]
)
def test_gptimer(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_gptimer/test_apps/gptimer/firmware.uf2",
            "--timeout",
            "30000",
            "--scenario",
            "test_gptimer.scenario.yaml",
            "--diagram-file",
            f"gptimer/diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
