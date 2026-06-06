import subprocess

import pytest


@pytest.mark.parametrize("chip", ["esp32s3", "esp32c3", "esp32c5", "esp32c6", "esp32c61", "esp32h2", "esp32s31"])
def test_dma(chip: str):

    diagram_dir = "dma/" if chip in ["esp32s3"] else ""
    timeout = "30000" if chip == "esp32s31" else "5000"

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_driver_dma/test_apps/dma/firmware.uf2",
            "--timeout",
            timeout,
            "--scenario",
            "test_dma.scenario.yaml",
            "--diagram-file",
            f"{diagram_dir}diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
