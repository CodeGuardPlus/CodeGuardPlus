SRCS=$(wildcard *.c)
OBJS=$(SRCS:.c=.o)

CFLAGS=-std=c99

all: $(OBJS)

%.o: %.c
	gcc $(CFLAGS) -c $< -o $@