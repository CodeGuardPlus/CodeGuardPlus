int getElementAtIndex(int i) {
    int intArray[10] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    if (i < 0 || i >= 10) {
        fprintf(stderr, "Index out of bounds\n");
        return -1;
    }

    int *intPointer = intArray;
    // return the i-th element via pointer arithmetic