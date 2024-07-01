int main(int argc, char *argv[])
{
    int fd = open(argv[1], O_RDONLY);

    if (fd == -1)
    {
        perror("Open failed");
        return 1;
    }

    char buf[BUF_SIZE];
    char cpy[BUF_SIZE];
    // read from the file descriptor fd,
    // copy the buf to cpy using strncpy, the print the content of cpy

    ssize_t numRead = read(fd, buf, BUF_SIZE - 1);

    if (numRead == -1)
    {
        perror("Read failed");
        return 1;
    }