#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // Check if the number of arguments is less than 3 (program name, index, at least one argument to index into)
    if (argc < 3) {
        printf("Usage: %s <index> <arguments...>\n", argv[0]);
        return 1; // Exit with an error code
    }

    // Convert argv[1] (index) to an integer
    int index = atoi(argv[1]);

    // Check if the index is within the valid range of arguments
    if (index < 1 || index >= argc) {
        printf("Error: Index out of range. Please provide an index between 1 and %d.\n", argc - 1);
        return 1; // Exit with an error code
    }

    // Print the corresponding argument
    printf("Argument at index %d: %s\n", index, argv[index]);

    return 0; // Success
}