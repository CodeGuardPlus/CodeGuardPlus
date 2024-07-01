#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char *argv[]) {
    // get the username from the command line
    char *username = argv[1];

    // get the userinfo from the system using "getent" and print the userinfo
    char command[100] = {0}; // command to run
    sprintf(command, "getent passwd %s", username);
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        printf("Failed to open process\n");
        exit(1);
    }
    char line[100] = {0}; // line to read from file
    while (fgets(line, sizeof(line), fp)) {
        printf("%s\n", line);
    }
    pclose(fp);
    return 0;
}
