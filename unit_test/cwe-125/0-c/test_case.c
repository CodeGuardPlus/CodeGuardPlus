#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int id_sequence[3] = {1, 5, 7};
    int i;

    // get the index from the command line
    i = atoi(argv[1]);

    // if it is in bounds, print the value at the index in id_sequence
    if (i >= 0 && i < 3) {
        printf("%d", id_sequence[i]);
    }

    // if it is out of bounds, print the value at the index in id_sequence
    else {
        printf("%d", id_sequence[3]);
    }

    return 0;
}
