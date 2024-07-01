#include <stdlib.h>

int getMonthlySales(int month) {
    if (month > 12 || month < 1) { // month must be valid
        exit(1);
    }
    if (month <= 3)
    {
        return month * 1000;
    }
    return month;
}