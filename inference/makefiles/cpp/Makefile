SRCS=$(wildcard *.cpp)   # Change the source files to look for .cpp files
OBJS=$(SRCS:.cpp=.o)     # Change the object file extension from .c to .cpp

CXX=g++                 # Use g++ as the C++ compiler
CXXFLAGS=-std=c++11     # Use C++11 standard, adjust if necessary

all: $(OBJS)            # The target that compiles all object files

%.o: %.cpp              # Rule to build .o files from .cpp files
	$(CXX) $(CXXFLAGS) -c $< -o $@