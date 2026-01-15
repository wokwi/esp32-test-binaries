import subprocess

import pytest


# ESP32-P4 currently fails some of the tests, so we exclude it.
@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_crypto(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/components/hal/test_apps/crypto/firmware.uf2",
            "--timeout",
            "60000",
            "--expect-text",
            "Tests finished, rc=0",
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
