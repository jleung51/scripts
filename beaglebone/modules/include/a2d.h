// This C module provides utility functions to access and control the
// A2D (analog to digital converter) on the Zen Cape.

#ifndef A2D_H
#define A2D_H

// Returns a value from 0 to 4095 linearly, representing raw voltage value.
int readVoltageRawFromChannel(unsigned int channel);

// Returns a value from 0 to 1.8 linearly, representing converted voltage value.
double readVoltageFromChannel(unsigned int channel);

#endif
