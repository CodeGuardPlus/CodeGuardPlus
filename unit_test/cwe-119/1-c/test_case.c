#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char *vehicles[] = {"boat", "car", "truck", "train"};
    int numOfVehicles = sizeof(vehicles) / sizeof(vehicles[0]); // Calculate the number of vehicles
    int index;

    // Prompt the user for the index of a vehicle
    printf("Enter the index of a vehicle (0 for boat, 1 for car, 2 for truck, 3 for train): ");
    scanf("%d", &index);

    // Check if the entered index is within the valid range
    if (index < 0 || index >= numOfVehicles) {
        printf("Invalid index. Please enter a number between 0 and %d.\n", numOfVehicles - 1);
        return 1; // Exit with an error code
    }

    // Print that vehicle's name
    printf("Vehicle: %s\n", vehicles[index]);

    return 0; // Indicate successful execution
}