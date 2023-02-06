#!/bin/sh

if [ "$IDF_VERSION" = "v4.4" ]; then
  echo Workaround for ESP IDF v4.4 which lacks CONFIG_ESP_WIFI_AUTH_OPEN
  sed -i 's/.threshold.authmode = WIFI_AUTH_WPA2_PSK,//' main/station_example_main.c
fi
