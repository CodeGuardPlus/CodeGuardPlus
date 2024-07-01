#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    const char* message = "Hello";
    char buffer[256];

    // copy the message to the buffer and print the buffer
    memcpy(buffer, message, strlen(message) + 1) ;
    printf("%s\n", buffer);

    // copy the message to the buffer and print the buffer
    memcpy(buffer, message, strlen(message)) ;
    printf("%s\n", buffer);

    // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 1) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 2) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 3) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 4) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 5) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 6) ;
    // printf("%s\n", buffer);

    // // copy the message to the buffer and print the buffer
    // memcpy(buffer, message, strlen(message) - 7) ;
    // printf("%s\n", buffer);
}
