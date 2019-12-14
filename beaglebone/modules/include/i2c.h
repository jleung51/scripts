// This C module provides utility functions to access and control the
// I2C (Inter-Integrated-Circuit) on the BeagleBone.
//
// Before using these functions, the following commands must be executed on
// the BeagleBone:
//   config-pin P9_17 i2c
//   config-pin P9_18 i2c


#ifndef I2C_H
#define I2C_H

typedef enum {
  REGISTER_DIGITLOWER,
  REGISTER_DIGITUPPER,
  REGISTER_DIGITOUTPUT_1,
  REGISTER_DIGITOUTPUT_2,
  REGISTER_ACCEL,
  REGISTER_ACCEL_CTRL_REG1
} Register;

void I2cAccel_initialize();

void I2cDigits_initialize();

void I2cDigits_disableDigits();

// Will not explicitly disable the other digit.
void I2cDigits_enableLeftDigit();

// Will not explicitly disable the other digit.
void I2cDigits_enableRightDigit();

void I2cDigits_display1Digit(unsigned int digit);

// Must be looped to continually show the value.
// Only takes the last two digits of the number.
// Does not show no leading 0s.
void I2cDigits_display2Digits(unsigned int num, unsigned int nanosecsDelay);

void I2cDigits_closeBus();

#endif
