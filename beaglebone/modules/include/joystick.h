#ifndef JOYSTICK
#define JOYSTICK

// ENUMS

typedef enum {
  NONE,
  LEFT,
  RIGHT,
  UP,
  DOWN
} JoystickDirection;

// Enables all the GPIO pins for each of the joystick inputs.
void Joystick_initialize();

JoystickDirection Joystick_read();
JoystickDirection Joystick_blockingRead();
void Joystick_blockUntilNeutral();

#endif
