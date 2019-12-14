// This C source file provides utility functions to access and control the
// A2D (analog to digital converter) on the Zen Cape.

#include <stdio.h>
#include <stdlib.h>

#include "../include/file.h"

#include "../include/a2d.h"

static const char *VOLTAGE_FILE =
    "/sys/bus/iio/devices/iio:device0/in_voltage%d_raw";
static const double REFERENCE_VOLTAGE = 1.8;
static const double MAX_VOLTAGE_RAW = 4095;
static const int BUFFER_MAX_LEN = 1024;

int readVoltageRawFromChannel(unsigned int channel) {
  // Create name of file to read from
  char filename[BUFFER_MAX_LEN];
  sprintf(filename, VOLTAGE_FILE, channel);

  // Read value from file
  char read_voltage_raw[BUFFER_MAX_LEN];
  readFromFile(filename, read_voltage_raw, BUFFER_MAX_LEN);

  return atoi(read_voltage_raw);
}

static double convertToVoltage(int read_voltage_raw) {
  double read_voltage_raw_d = (double) read_voltage_raw;

  // Limit value below/above
  if (read_voltage_raw_d < 0) {
    read_voltage_raw_d = 0;
  }
  else if (read_voltage_raw_d > MAX_VOLTAGE_RAW) {
    read_voltage_raw_d = MAX_VOLTAGE_RAW;
  }

  return read_voltage_raw_d / MAX_VOLTAGE_RAW * REFERENCE_VOLTAGE;
}

double readVoltageFromChannel(unsigned int channel) {
  return convertToVoltage(readVoltageRawFromChannel(channel));
}