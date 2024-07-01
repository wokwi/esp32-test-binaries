// SPDX-License-Identifier: Apache-2.0
// Wokwi SPI Flash chip emulation
// Copyright (c) 2024 Uri Shaked

#include "wokwi-api.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define DEBUG 0

#define STATUS_BUSY (1 << 0)
#define STATUS_WREN (1 << 1)

#define KB (1024)
#define MB (1024 * KB)

typedef enum {
  STATE_CMD,
  STATE_WRITE_REG,
  STATE_ADDR,
  STATE_DATA,
  STATE_DONE,
} spi_state_t;

typedef struct {
  pin_t cs_pin;
  uint16_t status_reg;
  uint8_t spi_buffer[4];
  uint8_t flash[4 * MB];
  spi_state_t state;
  spi_dev_t spi;
  uint8_t cmd;
  uint32_t addr;
} chip_state_t;

void on_cs_change(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *chip = (chip_state_t*)user_data;
  if (value == 0) {
    // CS went low, start SPI transaction
    chip->state = STATE_CMD;
    chip->spi_buffer[0] = 0;
    spi_start(chip->spi, chip->spi_buffer, 1); // Read command
  } else {
    spi_stop(chip->spi);
  }
}

static uint32_t handle_cmd(chip_state_t *chip, uint8_t cmd) {
  switch(cmd) {
    case 0x01: // WRSR - Write Status Register
      chip->state = STATE_WRITE_REG;
      return 1;
    
    case 0x02: // Page program
    case 0x20: // Block erase (4kb)
    case 0x52: // Block erase (32kb)
    case 0xd8: // Block erase (64kb)
    case 0x03: // Read sequential
    case 0x0b:
    case 0x3b:
    case 0x6b:
    case 0xbb:
    case 0xeb:
      chip->state = STATE_ADDR;
      return 3;

    case 0x04: // Write disable
      chip->state = STATE_DONE;
      chip->status_reg &= ~STATUS_WREN;
      return 0;

    case 0x05: // Read status
      chip->state = STATE_DONE;
      chip->spi_buffer[0] = chip->status_reg & 0xff;
      return 1;

    case 0x06: // Write enable
      chip->state = STATE_DONE;
      chip->status_reg |= STATUS_WREN;
      break;

    case 0x31: // Write status high (WRSR2)
      chip->state = STATE_WRITE_REG;
      return 1;

    case 0x35: // Read status high (RDSR2)
      chip->state = STATE_DONE;
      chip->spi_buffer[0] = chip->status_reg >> 8;
      break;

    case 0x9f: // Read chip ID
      chip->state = STATE_DONE;
      chip->spi_buffer[0] = 0xc8;
      chip->spi_buffer[1] = 0x40;
      chip->spi_buffer[2] = 0x16;
      chip->spi_buffer[3] = 0;
      return 3;
  }

  return 0;
}


void block_erase(chip_state_t *chip, uint32_t addr, uint32_t size) {
  uint32_t aligned_addr = addr & ~(size - 1);
  memset(chip->flash + aligned_addr, 0xff, size);
}

static void chip_spi_done(void *user_data, uint8_t *buffer, uint32_t count) {
  if (!count) {
    return;
  }

  chip_state_t *chip = (chip_state_t*)user_data;
  int transaction_size = 0;
  switch (chip->state) {
    case STATE_CMD:
      chip->cmd = buffer[0];
#if DEBUG
      printf("Got cmd: %02x (count: %d)\n", chip->cmd, count);
#endif
      buffer[0] = 0;
      transaction_size = handle_cmd(chip, chip->cmd);
      break;
    
    case STATE_WRITE_REG:
      switch (chip->cmd) {
        case 0x01: 
          chip->status_reg = (chip->status_reg & 0xff00) | buffer[0];
          chip->state = STATE_DONE;
          break;
        case 0x31:
          chip->status_reg = (chip->status_reg & 0x00ff) | buffer[0];
          break;
      }
      buffer[0] = 0;
      break;
    
    case STATE_ADDR:
      chip->addr = (buffer[0] << 16) | (buffer[1] << 8) | buffer[2];
#if DEBUG
      printf("Got addr: %08x\n", chip->addr);
#endif
      buffer[0] = 0;
      buffer[1] = 0;
      buffer[2] = 0;
      buffer[3] = 0;
      chip->state = STATE_DONE;

      switch (chip->cmd) {
        case 0x20: // Block erase (4kb)
          block_erase(chip, chip->addr, 4 * KB);
          break;
        case 0x52: // Block erase (32kb)
          block_erase(chip, chip->addr, 32 * KB);
          break;
        case 0xd8: // Block erase (64kb)
          block_erase(chip, chip->addr, 64 * KB);
          break;

        case 0x02: // Page program
        case 0x03: // Read sequential
        case 0x0b:
        case 0x3b:
        case 0x6b:
        case 0xbb:
        case 0xeb:
          chip->state = STATE_DATA;
          transaction_size = 4;
          memcpy(buffer, &chip->flash[chip->addr], sizeof(chip->spi_buffer));
          break;
      }
      break;

    case STATE_DATA:
      transaction_size = 4;
      switch (chip->cmd) {
        case 0x02: // Page program
#if DEBUG
          printf("Write %d bytes at %08x\n", count, chip->addr);
#endif
          memcpy(&chip->flash[chip->addr], buffer, count);
          chip->addr += count;
          break;
        case 0x03: // Read sequential
        case 0x0b:
        case 0x3b:
        case 0x6b:
        case 0xbb:
        case 0xeb:
#if DEBUG
          printf("Read %d bytes from %08x\n", count, chip->addr);
#endif
          chip->addr += count;
          memcpy(buffer, &chip->flash[chip->addr], sizeof(chip->spi_buffer));
          break;
      }
      break;

    case STATE_DONE:
      break;
  }
  
  if (pin_read(chip->cs_pin) == LOW) {
    spi_start(chip->spi, chip->spi_buffer, transaction_size);
  }
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));
  memset(chip->flash, 0xff, sizeof(chip->flash));
  chip->status_reg = 0;
  
  chip->cs_pin = pin_init("CS", INPUT_PULLUP);
  
  const pin_watch_config_t cs_watch_config = {
    .edge = BOTH,
    .pin_change = on_cs_change,
    .user_data = chip
  };
  pin_watch(chip->cs_pin, &cs_watch_config);

  const spi_config_t spi_config = {
    .sck = pin_init("SCK", INPUT),
    .mosi = pin_init("MOSI", INPUT),
    .miso = pin_init("MISO", INPUT),
    .mode = 0,
    .done = chip_spi_done,
    .user_data = chip,
  };

  chip->spi = spi_init(&spi_config);
}
