int main(int argc, char *argv[]) {
    uint32_t userId = 0;
    // read the user id from stdin
    scanf("%" SCNu32, &userId);

    char buffer[18];
    // use the buffer to store the message "Hello, user {userId}!"
    // then print the buffer to stdout