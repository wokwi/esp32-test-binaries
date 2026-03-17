import os
import subprocess

import pytest


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c5", "esp32c6", "esp32c61", "esp32h2", "esp32p4"]
)
def test_crypto(chip: str):
    diagram = f"crypto/diagram.{chip}.json"
    if not os.path.exists(diagram):
        diagram = f"diagram.{chip}.json"

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/esp_hal_security/test_apps/crypto/firmware.uf2",
            "--timeout",
            "60000",
            "--expect-text",
            "Tests finished, rc=0",
            "--diagram-file",
            diagram,
        ]
    )
    assert result.returncode == 0
