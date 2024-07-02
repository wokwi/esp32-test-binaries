import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32c3"]
)
def test_timer(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_timer/test_apps/firmware.uf2",
            "--timeout",
            "90000",
            "--scenario",
            "test_timer.scenario.yaml",
            "--diagram-file",
            f"timer/diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
