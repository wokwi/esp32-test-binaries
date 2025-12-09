import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_efuse(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/efuse/test_apps/firmware.uf2",
            "--timeout",
            "30000",
            "--scenario",
            "test_efuse.scenario.yaml",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
