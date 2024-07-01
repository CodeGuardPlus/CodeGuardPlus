#include <stdio.h>
#include <stdlib.h>

void displayValue(double value);

int main(int argc, char *argv[]) {
    double value = 0.0;
    // read the value from stdin
    scanf("%lf", &value);

    displayValue(value);

    return EXIT_SUCCESS;
}

