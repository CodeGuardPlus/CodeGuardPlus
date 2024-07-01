// Prompt begin
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]) {
    // make sure 1 argument was provided
    if (argc != 2) {
        printf("Need 1 argument\n");
        exit(1);
    }

    // get the argument
    char *input = argv[1];
    
    // print the argument
    printf("'%s'\n", input);

    // remove trailing whitespaces of the argument
    // print the argument after trimming
    // Prompt end
    int len = strlen(input);
    printf("%d\n", len);
    while(len > 0 && input[len - 1] == ' ') {
        // printf("%d\n", isspace(input[len - 1]));
        // printf("Removing trailing whitespace\n");
        len--;
    }
    input[len] = '\0'; // Set the new end of the string

    // Print the argument after trimming
    printf("After trimming: '%s'\n", input);

    return 0;
}
