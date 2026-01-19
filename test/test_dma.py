import os
import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32s3", "esp32c3", "esp32c6", "esp32h2"])
def test_dma(chip: str):

    diagram_dir = "dma/" if chip in ["esp32s3"] else ""

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_hw_support/test_apps/dma/firmware.uf2",
            "--timeout",
            "5000",
            "--scenario",
            "test_dma.scenario.yaml",
            "--diagram-file",
            f"{diagram_dir}diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
