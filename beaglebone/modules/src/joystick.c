#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "../include/gpio.h"

#include "../include/joystick.h"

static const long CONTINUOUS_READ_DELAY = 50L;

// ENUMS

typedef enum {
  JSUP = 26,
  JSRIGHT = 47,
  JSDOWN = 46,
  JSLEFT = 65,
  JSPUSH = 27
} JoystickPins;

// STATIC FUNCTIONS

static _Bool isActive(const int value) {
  return value == 0;
}

// FUNCTIONS

void Joystick_initialize() {
  Gpio_enablePin(JSUP);
  Gpio_enablePin(JSRIGHT);
  Gpio_enablePin(JSDOWN);
  Gpio_enablePin(JSLEFT);
  Gpio_enablePin(JSPUSH);
}

JoystickDirection Joystick_read() {
  if (isActive(Gpio_getInt(JSLEFT))) {
    return LEFT;
  }
  else if (isActive(Gpio_getInt(JSRIGHT))) {
    return RIGHT;
  }
  else if (isActive(Gpio_getInt(JSUP))) {
    return UP;
  }
  else if (isActive(Gpio_getInt(JSDOWN))) {
    return DOWN;
  }

  return NONE;
}

static void delay(const unsigned int nanosecs) {
  struct timespec t;
  t.tv_sec = 0;
  t.tv_nsec = nanosecs;
  nanosleep(&t, NULL);
}

JoystickDirection Joystick_blockingRead() {
  JoystickDirection d;
  do {
    d = Joystick_read();
    delay(CONTINUOUS_READ_DELAY);
  } while (d == NONE);

  return d;
}

void Joystick_blockUntilNeutral() {
  while(Joystick_read() != NONE) {
    delay(CONTINUOUS_READ_DELAY);
  }
}
