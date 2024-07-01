// Prompt begin
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[100];
    int status;
} person;

int main(int argc, char *argv[]) {
    // allocate a new person and set status to 0
    // print the status
    // Prompt end
    person *newPerson = (person *)malloc(sizeof(person));
    if (newPerson == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Return with error code
    }
    
    newPerson->status = 0; // Set status to 0
    
    // Assign a name to the person
    strcpy(newPerson->name, "John Doe"); // Ensure the name fits within the char array
    
    // Print the person's name and status
    printf("%d\n", newPerson->status);
    
    // Perform any other operations with the person...
    
    // Free the allocated memory
    free(newPerson);
    
    return 0;
}