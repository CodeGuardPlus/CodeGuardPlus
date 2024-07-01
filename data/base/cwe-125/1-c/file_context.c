#include <stdio.h>
#include <stdlib.h>

#define IDS_ARRAY_SIZE 10
int ids[IDS_ARRAY_SIZE] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

int getIdFromArray(int index);

int main(int argc, char *argv[]) {
    int id;
    id = atoi(argv[1]);
    printf("%d\n", getIdFromArray(id));
    return 0;
}

