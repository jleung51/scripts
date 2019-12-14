#include <stdio.h>

#include "../include/pwl.h"

const double A2D_VALUES[10] =
    {0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4100};
const double ARRAY_SIZE_VALUES[10] =
    {1, 20, 60, 120, 250, 300, 500, 800, 1200, 2100};
const int A2D_TO_ARRAY_LEN = 10;

int a2dToArraySize(int a2dValue) {
  // Cap maximum/minimum sizes
  if (a2dValue < 0) {
    a2dValue = 0;
  }
  else if (a2dValue > 4095) {
    a2dValue = 4095;
  }

  for (int i = 1; i < A2D_TO_ARRAY_LEN; ++i) {
    if (a2dValue < A2D_VALUES[i]) {
      double x1 = A2D_VALUES[i-1];
      double x2 = A2D_VALUES[i];
      double y1 = ARRAY_SIZE_VALUES[i-1];
      double y2 = ARRAY_SIZE_VALUES[i];

      double convertRatio = (y2-y1) / (x2-x1);

      // Calculate using equation of a line
      double yIntercept = y1 - convertRatio * x1;

      // y = ax+b equation
      return a2dValue * convertRatio + yIntercept;
    }
  }
  return 0;
}