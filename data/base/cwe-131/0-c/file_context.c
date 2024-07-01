#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *my_strdup(const char *str);

int main(int argc, char *argv[])
{
    char *str = my_strdup(argv[1]);
    printf("%s\n", str);
    free(str);
    return 0;
}