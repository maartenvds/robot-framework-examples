# Author: Maarten Vandersteegen
# Make a shared picotcp library with an additional wrapper

TARGET=libpicotcp.so
PICOTCPDIR?=../../../PicoTCP/picotcp
EXTRAOBJ=wrapper.o
PICOBUILD=build
INC=-I $(PICOBUILD)/include
CFLAGS=-Wall -fPIC
CC=gcc

all: $(TARGET)

$(TARGET): $(PICOBUILD) $(EXTRAOBJ)
	$(CC) -shared -o $(TARGET) $(EXTRAOBJ) $(PICOBUILD)/lib/*.o $(PICOBUILD)/modules/*.o

$(PICOBUILD):
	make -C $(PICOTCPDIR) TUN=1 ARCH=shared

.c.o: 
	$(CC) -c $(CFLAGS) $(INC) $< -o $@

clean:
	rm -rf $(TARGET) $(EXTRAOBJ) $(PICOBUILD)
