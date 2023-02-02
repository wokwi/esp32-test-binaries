#!/bin/sh

build() {
  IDF_VERSION="$1"
  APP_PATH="$2"
  CHIPS="$3"
  for CHIP in $CHIPS; do
    TARGET_DIR=bin/$CHIP/idf/$IDF_VERSION/$APP_PATH
    mkdir -p $TARGET_DIR
    echo $(pwd)/config/$APP_PATH
    docker run -e "IDF_TARGET=$CHIP" -v "$(pwd)/$TARGET_DIR:/output" -v "$(pwd)/cache/${IDF_VERSION}:/root/.ccache" \
      -v "$(pwd)/config/$APP_PATH:/config:ro" \
      -it espressif/idf:$IDF_VERSION \
      /bin/bash -c "cd /opt/esp/idf && cd $APP_PATH && cp /config/* . && idf.py uf2 && \
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
  build v5.0 "$APP" "esp32 esp32s2 esp32s3 esp32c2 esp32c3"
  build latest $APP "esp32 esp32s2 esp32s3 esp32c2 esp32c3 esp32c6"
done
