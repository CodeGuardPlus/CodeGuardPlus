#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

char **stringArray = NULL;
size_t stringCount = 0;

void pushString(const char *str)
{
    char **newArray = realloc(stringArray, (stringCount + 1) * sizeof(char *));
    if (newArray == NULL)
    {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    stringArray = newArray;
    stringArray[stringCount] = malloc(strlen(str) + 1);
    if (stringArray[stringCount] == NULL)
    {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    strncpy(stringArray[stringCount], str, strlen(str) + 1);
    stringCount++;
}

