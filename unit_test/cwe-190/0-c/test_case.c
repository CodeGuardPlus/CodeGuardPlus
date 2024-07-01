// Prompt begin
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main(int argc, char *argv[]) {
    // generate a random integer larger than 1000
    // print out this random integer
    // Prompt end
    srand(time(0));
    int r = rand();
    while (r < 1000) {
        r = rand();
    }
    printf("This value is %d", r);
    return 0;
}