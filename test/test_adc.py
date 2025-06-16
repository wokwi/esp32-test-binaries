import subprocess

import pytest

expected_adc1_3 = "EXAMPLE: ADC1 Channel[3] Raw Data: 2050"
expected_adc2_0 = "EXAMPLE: ADC2 Channel[0] Raw Data: 2050"

expected_text = {
    "esp32": expected_adc2_0,
    "esp32s2": expected_adc2_0,
    "esp32s3": expected_adc2_0,
    "esp32c3": expected_adc1_3,
    "esp32c6": expected_adc1_3,
    "esp32h2": expected_adc1_3,
    "esp32p4": expected_adc2_0,
}


@pytest.mark.parametrize(
    "chip", ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32h2", "esp32p4"]
)
def test_adc(chip: str):

    # Run the Wokwi CLI
    result = subprocess.run(
        [
            "wokwi-cli",
            "--elf",
            f"../bin/{chip}/idf/latest/examples/peripherals/adc/oneshot_read/firmware.uf2",
            "--timeout",
            "5000",
            "--expect-text",
            expected_text[chip],
            "--diagram-file",
            f"diagram.{chip}.json",
        ]
    )
    assert result.returncode == 0
