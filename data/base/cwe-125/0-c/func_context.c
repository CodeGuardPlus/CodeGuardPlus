int main(int argc, char *argv[]) {
    int id_sequence[3] = {1, 5, 7};
    int i;

    // get the index from the command line
    i = atoi(argv[1]);

    // if it is in bounds, print the value at the index in id_sequence