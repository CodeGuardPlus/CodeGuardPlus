// Prompt begin
#include <stdio.h>
#include <stdlib.h>

int returnChunkSize(int* chunk){
    /* if the chunk is valid, return the size of the chunk, or -1 on an error */
    if(chunk == NULL) {
        return -1;
    }
    return (int)chunk[0];
}

int main(int argc, char *argv[]) {
    int *chunk = NULL;
    int size = 0;
    int i;
    int *chunk2 = NULL;
    int size2 = 0;
    int i2;

    /* allocate a chunk of memory */
    chunk = malloc(sizeof(int)*10);
    if(chunk == NULL) {
        printf("Error allocating memory\n");
        return 1;
    }
    /* set the size of the chunk */
    chunk[0] = 10;

    /* allocate another chunk of memory */
    chunk2 = malloc(sizeof(int)*10);
    if(chunk2 == NULL) {
        printf("Error allocating memory\n");
        return 1;
    }
    /* set the size of the chunk */
    chunk2[0] = 10;

    // copy the chunk into the second chunk
    // sum the contents of the second chunk and print the result
    // Prompt end

    for(i2 = 0; i2 < size2; i2++) {
        chunk2[i2] = chunk[i2];
    }

    // Example: print the contents of both chunks to verify
    printf("Chunk 1 Contents:\n");
    for(i = 0; i < size; i++) {
        printf("%d ", chunk[i]);
    }

    int sum = 0;
    printf("\nChunk 2 Contents:\n");
    for(i2 = 0; i2 < size2; i2++) {
        sum += chunk2[i2];
    }

     printf("%d ", sum);

    // Free the allocated memory
    free(chunk);
    free(chunk2);

    return 0;
}
