#include <stdio.h>
#include <stdlib.h>

#include "../include/file.h"

void readFromFile(
    char* filename,
    char* buffer,
    const unsigned int max_length) {

  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    printf("Error: Unable to open file %s for reading.\n", filename);
    exit(-1);
  }

  // Read data immediately
  fgets(buffer, max_length, file);
  fclose(file);
}

void writeIntToFile(char* filename, const int data) {
  FILE *file = fopen(filename, "w");
  if (file == NULL) {
    printf("Error: Unable to open file %s for writing.\n", filename);
    exit(1);
  }
  // Write data to file immediately
  fprintf(file, "%d", data);
  fclose(file);
}

void writeStringToFile(char* filename, const char* data) {
  FILE *file = fopen(filename, "w");
  if (file == NULL) {
    printf("Error: Unable to open file %s for writing.\n", filename);
    exit(1);
  }
  // Write data to file immediately
  fprintf(file, "%s", data);
  fclose(file);
}
