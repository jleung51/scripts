// This C source file provides utility functions to access and control the
// I2C (Inter-Integrated-Circuit) on the BeagleBone.

#include <fcntl.h>  // For O_RDWR
#include <linux/i2c.h>
#include <linux/i2c-dev.h>  // For I2C_SLAVE
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <time.h>
#include <unistd.h>

#include "../include/gpio.h"

#include "../include/i2c.h"

typedef enum {
  BUS0,
  BUS1,
  BUS2
} I2cBus;

static const int BUFFER_LEN = 1024;

static const char DIGIT_PORT_VAL_OUTPUT = 0x00;
static const char ACCEL_VAL_ACTIVE = 0x01;

static const int PIN_LEFT = 61;
static const int PIN_RIGHT = 44;

static const char I2C_DEVICE_ADDRESS = 0x20;

// Stores all opened file descriptors.
static int BusFileDescriptors[3] = {0, 0, 0};

static void delay(const unsigned int nanosecs) {
  struct timespec t;
  t.tv_sec = 0;
  t.tv_nsec = nanosecs;
  nanosleep(&t, NULL);
}

static void getFileOfBus(I2cBus b, char *filename) {
  sprintf(filename, "/dev/i2c-%d", b);
}

static unsigned char toRegisterAddress(Register r) {
  if (r == REGISTER_DIGITLOWER) {
    return 0x14;
  }
  else if (r == REGISTER_DIGITUPPER) {
    return 0x15;
  }
  else if (r == REGISTER_DIGITOUTPUT_1) {
    return 0x00;
  }
  else if (r == REGISTER_DIGITOUTPUT_2) {
    return 0x01;
  }
  else if (r == REGISTER_ACCEL) {
    return 0x1C;
  }
  else if (r == REGISTER_ACCEL_CTRL_REG1) {
    return 0x2A;
  }
  return 0;
}

// Takes hexadecimal values which represent half of the
// segments from the display.
static void writeValueToRegister(Register r, unsigned char value) {
  int registerBufferLen = 2;
  unsigned char buffer[2] = {toRegisterAddress(r), value};

  int result = write(BusFileDescriptors[BUS1], buffer, registerBufferLen);
  if (result != registerBufferLen) {
    char msg[BUFFER_LEN];
    sprintf(msg, "Unable to write to I2C bus %d, register %u.", BUS1, r);
    perror(msg);
    exit(1);
  }
}



void I2cAccel_initialize() {
  // Initialize bus
  char filename[BUFFER_LEN];
  getFileOfBus(BUS1, filename);

  int fileDescriptor = open(filename, O_RDWR);
  int result = ioctl(fileDescriptor, I2C_SLAVE, toRegisterAddress(REGISTER_ACCEL));
  if (result < 0) {
    perror("Unable to set I2C device to slave address.");
    exit(1);
  }

  // Set to array value in static variables
  BusFileDescriptors[BUS1] = fileDescriptor;

  // Set device to ACTIVE
  writeValueToRegister(REGISTER_ACCEL_CTRL_REG1, ACCEL_VAL_ACTIVE);
}

void I2cDigits_initialize() {
  // Turn on I2C configurations for the pins
  system("config-pin P9_17 i2c");
  system("config-pin P9_18 i2c");

  // Export, set to output, and turn on
  Gpio_enablePinOutput(PIN_LEFT);
  Gpio_enablePinOutput(PIN_RIGHT);
  Gpio_setValue(PIN_LEFT, 1);
  Gpio_setValue(PIN_RIGHT, 1);

  // Initialize bus
  char filename[BUFFER_LEN];
  getFileOfBus(BUS1, filename);

  int fileDescriptor = open(filename, O_RDWR);
  int result = ioctl(fileDescriptor, I2C_SLAVE, I2C_DEVICE_ADDRESS);

  if (result < 0) {
    perror("Unable to set I2C device to slave address.");
    exit(1);
  }

  // Set to array value in static variables
  BusFileDescriptors[BUS1] = fileDescriptor;

  // Enable I2C outputs
  writeValueToRegister(REGISTER_DIGITOUTPUT_1, DIGIT_PORT_VAL_OUTPUT);
  writeValueToRegister(REGISTER_DIGITOUTPUT_2, DIGIT_PORT_VAL_OUTPUT);
}

void I2cDigits_disableDigits() {
  Gpio_setValue(PIN_LEFT, 0);
  Gpio_setValue(PIN_RIGHT, 0);
}

void I2cDigits_enableLeftDigit() {
  // Enable pins as GPIO, set as output, and enable value
  Gpio_enablePinOutput(PIN_LEFT);
  Gpio_setValue(PIN_LEFT, 1);
}

void I2cDigits_enableRightDigit() {
  // Enable pins as GPIO, set as output, and enable value
  Gpio_enablePinOutput(PIN_RIGHT);
  Gpio_setValue(PIN_RIGHT, 1);
}

void I2cDigits_display1Digit(unsigned int digit) {
  // Take only rightmost digit
  if (digit > 9) {
    digit %= 10;
  }

  unsigned char upper = 0;
  unsigned char lower = 0;

  // Set to values which display a digit
  switch (digit) {
    case 0:
      upper = 0x87;
      lower = 0xa1;
      break;
    case 1:
      upper = 0x21;
      lower = 0x04;
      break;
    case 2:
      upper = 0x0F;
      lower = 0x31;
      break;
    case 3:
      upper = 0x07;
      lower = 0xb0;
      break;
    case 4:
      upper = 0x8b;
      lower = 0x90;
      break;
    case 5:
      upper = 0x8c;
      lower = 0xb0;
      break;
    case 6:
      upper = 0x8c;
      lower = 0xb1;
      break;
    case 7:
      upper = 0x15;
      lower = 0x04;
      break;
    case 8:
      upper = 0x8f;
      lower = 0xb1;
      break;
    case 9:
    default:
      upper = 0x8f;
      lower = 0x90;
  }

  writeValueToRegister(REGISTER_DIGITUPPER, upper);
  writeValueToRegister(REGISTER_DIGITLOWER, lower);
}

void I2cDigits_display2Digits(unsigned int num, unsigned int nanosecsDelay) {
  // Cap at 99
  num = (num > 99) ? 99 : num;
  unsigned int digit1 = num/10;
  unsigned int digit2 = num % 10;

  I2cDigits_disableDigits();
  I2cDigits_enableLeftDigit();
  I2cDigits_display1Digit(digit1);
  delay(nanosecsDelay);

  I2cDigits_disableDigits();
  I2cDigits_enableRightDigit();
  I2cDigits_display1Digit(digit2);
  delay(nanosecsDelay);
}

void I2cDigits_closeBus() {
  close(BusFileDescriptors[BUS1]);
}