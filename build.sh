#!/bin/sh

ALL_CHIPS="esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6 esp32h2 esp32p4"

build() {
  IDF_VERSION="$1"
  APP_PATH="$2"
  CHIPS="$3"
  if [ -n "$BUILD_IDF_VERSION" ] && [ "$BUILD_IDF_VERSION" != "$IDF_VERSION" ]; then
    return # Skip
  fi
  for CHIP in $CHIPS; do
    TARGET_DIR=bin/$CHIP/idf/$IDF_VERSION/$APP_PATH
    mkdir -p $TARGET_DIR
    echo $(pwd)/config/$APP_PATH
    docker run --rm -e "IDF_TARGET=$CHIP" -e "IDF_VERSION=$IDF_VERSION" \
      -v "$(pwd)/$TARGET_DIR:/output" -v "$(pwd)/cache/${IDF_VERSION}:/root/.ccache" \
      -v "$(pwd)/config/$APP_PATH:/config:ro" \
      espressif/idf:$IDF_VERSION \
      /bin/bash -c "\
        cd /opt/esp/idf && cd $APP_PATH && cp /config/* . && \
        (if [ -e "precompile.sh" ]; then ./precompile.sh; fi) && \
        idf.py uf2 && \
        cp build/uf2.bin /output/firmware.uf2 && git rev-parse HEAD > /output/commit.txt" && \
    docker inspect --format='{{index .RepoDigests 0}}' espressif/idf:$IDF_VERSION > $TARGET_DIR/image.txt
  done
}

APPS="  
  examples/get-started/hello_world
  examples/wifi/getting_started/station
  examples/wifi/getting_started/softAP
"

for APP in $APPS; do
  build release-v5.0 "$APP" "esp32 esp32s2 esp32s3 esp32c2 esp32c3"
  build release-v5.1 "$APP" "esp32 esp32s2 esp32s3 esp32c2 esp32c3"
  build release-v5.2 "$APP" "esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6"
  build latest $APP "esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6"
  if [ "$APP" = "examples/get-started/hello_world" ]; then
    build release-v5.1 "$APP" "esp32h2"
    build release-v5.2 "$APP" "esp32h2"
    build latest "$APP" "esp32h2 esp32p4"
  fi
done

build latest examples/peripherals/i2c/i2c_simple "$ALL_CHIPS"
build latest examples/peripherals/spi_slave/sender "$ALL_CHIPS"
build latest components/mbedtls/test_apps "$ALL_CHIPS"
build latest components/hal/test_apps/crypto "$ALL_CHIPS"
build latest components/esp_driver_ledc/test_apps/ledc "$ALL_CHIPS"
build latest components/esp_psram/test_apps/psram "esp32 esp32s2 esp32s3 esp32p4"
build latest components/esp_driver_pcnt/test_apps/pulse_cnt "esp32 esp32s2 esp32s3 esp32c6 esp32h2 esp32p4"
build latest components/esp_wifi/test_apps/wifi_function "esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6"
build latest examples/peripherals/rmt/led_strip "$ALL_CHIPS"
build latest examples/peripherals/ledc/ledc_basic "$ALL_CHIPS"
build latest examples/peripherals/adc/oneshot_read "esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6 esp32h2"
build latest examples/peripherals/usb/device/tusb_console "esp32s2 esp32s3 esp32p4"
build latest examples/peripherals/usb_serial_jtag/usb_serial_jtag_echo "esp32s3 esp32c3 esp32c6 esp32h2 esp32p4"