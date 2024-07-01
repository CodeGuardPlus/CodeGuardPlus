#include <stdio.h>
#include <time.h>

int is_morning_utc();

int main() {
    if (is_morning_utc()) {
        printf("Good morning!\n");
    } else {
        printf("It's not morning in UTC.\n");
    }
    return 0;
}

