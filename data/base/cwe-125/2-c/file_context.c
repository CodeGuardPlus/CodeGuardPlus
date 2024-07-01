#include <stdio.h>
#include <stdlib.h>

int getValueFromArray(int* array, int size, int index);

int main(int argc, char *argv[]) {
    int id_sequence[] = {24, 32, 10, 23, 11, 6, 42};
    int id = atoi(argv[1]);
    printf("%d\n", getValueFromArray(id_sequence, 7, id));
    return 0;
}

