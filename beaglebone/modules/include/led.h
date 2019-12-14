#ifndef LED
#define LED

// ENUMS

typedef enum {
  LED0 = 0,
  LED1 = 1,
  LED2 = 2,
  LED3 = 3
} LedNumber;

// FUNCTIONS

// This function sets trigger to 0 to "none" and turns off all LEDs.
void Led_reset();

void Led_turnOn(LedNumber num);
void Led_turnOnAll();
void Led_turnOff(LedNumber num);
void Led_turnOffAll();

void Led_flashAll(const unsigned int nanosecs);

#endif
