// This C source file provides utility functions to access and modify the
// Beaglebone GPIO pins.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "../include/fileIO.h"

#include "../include/gpio.h"

const unsigned int MAX_STR_LEN = 1024;

static void delay(const unsigned int nanosecs) {
  struct timespec t;
  t.tv_sec = 0;
  t.tv_nsec = nanosecs;
  nanosleep(&t, NULL);
}

// Access functions

void Gpio_getString(const unsigned int pin, char* buffer) {

  // Format pin into string filename
  char filename[MAX_STR_LEN];
  sprintf(filename, "/sys/class/gpio/gpio%d/value", pin);

  writeToFile(filename, buffer);
}

int Gpio_getInt(const unsigned int pin) {
  char buffer[MAX_STR_LEN];
  Gpio_getString(pin, buffer);
  return atoi(buffer);
}

// Modification functions

void Gpio_enablePin(const unsigned int pin) {
  writeIntToFile("/sys/class/gpio/export", pin);
}

void Gpio_enablePinOutput(const unsigned int pin) {
  Gpio_enablePin(pin);

  char filename[1024];
  sprintf(filename, "/sys/class/gpio/gpio%d/direction", pin);
  writeToFile(filename, "out");
}

void Gpio_finishEnabling() {
  delay(300000000);  // 300 ms
}

void Gpio_disablePin(const unsigned int pin) {
  writeIntToFile("/sys/class/gpio/unexport", pin);
}

void Gpio_setValue(const unsigned int pin, const int value) {
  // Format pin into string filename
  char filename[1024];
  sprintf(filename, "/sys/class/gpio/gpio%d/value", pin);

  writeIntToFile(filename, value);
}
