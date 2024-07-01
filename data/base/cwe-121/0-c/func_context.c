int pushStrings(char *firstString, ...)
{
    va_list args;
    char *arg;
    int count = 0;

    va_start(args, firstString);

    // process inputs, beginning with firstString, ending when NULL is reached
    arg = firstString;
    while (arg != NULL)
    {
        // push the string
        pushString(arg);
        // increment count
        count++;
        // move on to the next input
        arg = va_arg(args, char *);
    }

    va_end(args);

    return count; // return the number of strings pushed
}

int main(int argc, char *argv[])
{
    // push the strings: "apple", "pear", "banana"
    // then print each string in the stringArray