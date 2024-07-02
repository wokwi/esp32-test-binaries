import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_i2c(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_i2c/test_apps/i2c_test_apps/firmware.uf2",
            "--timeout",
            "5000",
            "--scenario",
            "test_i2c.scenario.yaml",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
