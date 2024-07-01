#include <stdio.h>
#include <stdlib.h>

int getElementAtIndex(int i);

int main(int argc, char *argv[]) {
    int index = atoi(argv[1]);

    int value = getElementAtIndex(index);
    printf("%d\n", value);

    return 0;
}

