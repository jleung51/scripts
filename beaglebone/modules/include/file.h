#ifndef FILE_H
#define FILE_H

void readFromFile(
    char* filename,
    char* buffer,
    const unsigned int max_length);

void writeIntToFile(char* filename, const int data);
void writeStringToFile(char* filename, const char* data);

#endif
