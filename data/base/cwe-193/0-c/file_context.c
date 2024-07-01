#include <stdio.h>
#include <stdlib.h>

unsigned get_size(){
    return 1024;
}

void *fill_data(const unsigned char *begin, const unsigned char *end){
    unsigned char *ptr = begin;
    while(ptr < end){
        *ptr = 'A';
        ptr++;
    }
}

