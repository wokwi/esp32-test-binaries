import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2"]
)
def test_spi_master(chip: str):
    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_spi/test_apps/master/firmware.uf2",
            "--timeout",
            "25000",
            "--scenario",
            "../test_spi_master.scenario.yaml",
            "--diagram-file",
            f"diagram.{chip}.json",
            "./spi_master",
        ]
    )
    assert result.returncode == 0
