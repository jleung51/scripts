#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "../include/file.h"

#include "../include/led.h"

static const int LED_TOTAL = 4;

// FUNCTIONS

void Led_reset() {
  char filename[100];
  for (int i = 0; i < LED_TOTAL; ++i) {
    // Deactivate blinking
    sprintf(filename, "/sys/class/leds/beaglebone:green:usr%d/trigger", i);
    writeStringToFile(filename, "none");

    Led_turnOff(i);
  }
}

void Led_turnOn(LedNumber led) {
  char filename[100];
  sprintf(filename, "/sys/class/leds/beaglebone:green:usr%d/brightness", led);
  writeIntToFile(filename, 1);
}

void Led_turnOnAll() {
  for (int i = 0; i < LED_TOTAL; ++i) {
    Led_turnOn(i);
  }
}

void Led_turnOff(LedNumber led) {
  char filename[100];
  sprintf(filename, "/sys/class/leds/beaglebone:green:usr%d/brightness", led);
  writeIntToFile(filename, 0);
}

void Led_turnOffAll() {
  for (int i = 0; i < LED_TOTAL; ++i) {
    Led_turnOff(i);
  }
}

static void delay(const unsigned int nanosecs) {
  struct timespec t;
  t.tv_sec = 0;
  t.tv_nsec = nanosecs;
  nanosleep(&t, NULL);
}

void Led_flashAll(const unsigned int nanosecs) {
  Led_turnOnAll();
  delay(nanosecs);
  Led_turnOffAll();
}
