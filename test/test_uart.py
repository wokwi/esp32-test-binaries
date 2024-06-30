import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2"]
)
def test_uart(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_uart/test_apps/uart/firmware.uf2",
            "--timeout",
            "30000",
            "--scenario",
            "test_uart.scenario.yaml",
            "--diagram-file",
            f"uart/diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
