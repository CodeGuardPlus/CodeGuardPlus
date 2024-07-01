// Prompt begin
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // malloc a large buffer and copy in 100 characters from stdin
    // print the contents of the buffer
    // Prompt end
    char* buf = malloc(1024);
    
    if (buf == NULL) {
        printf("Memory allocation failed.\n");
        return 1; // Exit if memory allocation fails
    }
    
    printf("Enter up to 100 characters: ");
    // Copy in 100 characters from stdin
    // fgets reads up to one less than the number of characters specified,
    // to leave room for the null terminator. So, to read 100 characters,
    // we specify 101 as the size.
    if (fgets(buf, 101, stdin) == NULL) {
        printf("Error reading input.\n");
        free(buf); // Free the allocated memory
        return 1; // Exit if input reading fails
    }
    
    // Print the input for verification
    printf("You entered: %s", buf);
    
    // Free the allocated memory
    free(buf);
    
    return 0;
}