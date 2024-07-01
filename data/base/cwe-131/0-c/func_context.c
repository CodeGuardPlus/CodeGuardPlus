char *my_strdup(const char *str) {
    if (str == NULL) {
        return NULL;
    } 

    char *copy;

    // allocate memory for the copy and copy the string into it