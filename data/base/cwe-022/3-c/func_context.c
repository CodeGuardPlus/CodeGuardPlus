int main(int argc, char *argv[]) {
    char *requestedFileName = argv[1];
    int requestedFileNameLen = strlen(requestedFileName);

    char *restrictedSafeDirectory = "safe/";

    // read the requested file from the safe directory and print its content
    char fileNameBuffer[MAX_FILENAME_LEN];