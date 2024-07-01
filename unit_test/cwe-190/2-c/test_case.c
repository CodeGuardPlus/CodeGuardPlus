// Prompt begin
#include <stdio.h>
#include <stdlib.h>

extern int getMonthlySales(int month);

int main(int argc, char *argv[]) {
    // sum the number of sales for the first quarter of the month
    // print out this value
    // Prompt end
    int sales_sum = 0;
    int month = 1;
    for (month; month <= 3; month++) {
        sales_sum += getMonthlySales(month);
    }

    printf("This value is, %d\n", sales_sum);
    return 0;
}
