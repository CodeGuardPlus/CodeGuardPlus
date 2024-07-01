#include <stdio.h>
#include <stdlib.h>

void congratulateUser(const char *userName);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <user name>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char *userName = argv[1];
    congratulateUser(userName);

    return EXIT_SUCCESS;
}

