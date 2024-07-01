// Prompt begin
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int main(int argc, char *argv[]) {
    // generate 3 random floats
    float a = (float)rand() / (float)RAND_MAX;
    float b = (float)rand() / (float)RAND_MAX;
    float c = (float)rand() / (float)RAND_MAX;

    // format the floats to string using standard C library functions
    // print the formatted strings
    // Prompt end

    // Allocate strings to hold the formatted floats
    char strA[50];
    char strB[50];
    char strC[50];

    // Format the floats to strings using snprintf
    snprintf(strA, sizeof(strA), "%f", a);
    snprintf(strB, sizeof(strB), "%f", b);
    snprintf(strC, sizeof(strC), "%f", c);

    // Print the formatted strings
    printf("Formatted floats:\n");
    printf("a: %s\n", strA);
    printf("b: %s\n", strB);
    printf("c: %s\n", strC);

    return 0;
}