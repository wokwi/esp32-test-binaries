import os
import subprocess

import pytest

# read from process.env or use default values
IDF_VERSION = os.getenv("IDF_VERSION", "latest")

ALL_CHIPS = ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c5", "esp32c6", "esp32h2", "esp32p4"]

IDF_VERSIONS = {
    "release-v4.4": ["esp32", "esp32s2", "esp32s3", "esp32c3"],
    "release-v5.0": ["esp32", "esp32s2", "esp32s3", "esp32c3"],
    "release-v5.1": ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32h2"],
    "release-v5.2": ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2"],
    "release-v5.3": ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2"],
    "release-v5.4": ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"],
    "latest": ALL_CHIPS,
}


@pytest.mark.parametrize("chip", ALL_CHIPS)
def test_hello_world(chip: str):
    supported_chips = IDF_VERSIONS.get(IDF_VERSION)
    if supported_chips is not None and chip not in supported_chips:
        pytest.skip(f"Chip {chip} not supported in IDF version {IDF_VERSION}")

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/{IDF_VERSION}/examples/get-started/hello_world/firmware.uf2",
            "--timeout",
            "2000",
            "--diagram-file",
            f"diagram.{chip}.json",
            "--expect-text",
            "Restarting in 9 seconds...",
        ]
    )
    assert result.returncode == 0
