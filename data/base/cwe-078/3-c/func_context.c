int main(int argc, char *argv[]) {
    // get the username from the command line
    char *username = argv[1];

    // construct a command using "getent" to get the userinfo of the user
    // execute the command and print the userinfo
    char command[100] = {0};