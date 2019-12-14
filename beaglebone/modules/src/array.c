#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

#include "../include/array.h"


int *createArray(int len)
{
    int *arr = malloc(len * sizeof(int));
   
    for (int i = 0; i < len; i++) {
        arr[i] = i;
    }

    for (int j = 0; j < len; j++) {
        int newIndex = rand() % len;
        if (j != newIndex) {
            int temp = arr[j];
            arr[j] = arr[newIndex];
            arr[newIndex] = temp;
        }
    }
    return arr;
}

// Referenced https://www.geeksforgeeks.org/bubble-sort/
void bubbleSort(int* arr, int len)
{
    for (int i = 0; i < len-1; i++) {
        for (int j = 0; j < len-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
    }
    free(arr);
}