int main(int argc, char* argv[]) {
    // Get the size of the data block we need to allocate
    unsigned size = get_size();
    // Allocate the data block
    unsigned char *data = (unsigned char *)malloc(size);
    if (data == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    unsigned char *end = data + size;
    // Fill the data block with 'A's
    fill_data(data, end);

    // Ensure the last byte is null-terminated, then print the data block