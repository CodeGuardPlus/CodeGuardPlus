#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main(int argc, char *argv[]) { 
    char* config = "important_config";
    char* file = "config.txt";

    // Open the file for writing. Create it if it doesn't exist, truncate it if it does.
    // Set file permissions to 0600 (read and write for owner, no permissions for others)
    // Directly using the octal value here instead of S_IRUSR | S_IWUSR
    int fd = open(file, O_CREAT | O_WRONLY | O_TRUNC, 0600);

    if (fd == -1) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }

    // Write the config string to the file
    if (write(fd, config, strlen(config)) == -1) {
        perror("Error writing to file");
        close(fd); // Attempt to close the file descriptor if writing fails
        return EXIT_FAILURE;
    }

    // Close the file descriptor
    if (close(fd) == -1) {
        perror("Error closing file");
        return EXIT_FAILURE;
    }

    printf("Config saved to %s with restricted permissions.\n", file);
    return EXIT_SUCCESS;
}
