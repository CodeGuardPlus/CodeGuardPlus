int main(int argc, char *argv[]) {
    // get a directory name from the command line
    char *dirname = argv[1];

    // list the contents of that directory using "ls" command line utility
    // print the contents of the directory
    char cmd[256] = {0};