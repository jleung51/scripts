#ifndef ARRAY_H
#define ARRAY_H

// Creates an allocated array which must be freed by the caller.
int *createArray(int len);

void bubbleSort(int *arr, int len);

#endif