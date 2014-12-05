# Author: Maarten Vandersteegen
# Make a shared picotcp library with an additional wrapper

TARGET=libpicotcp.so
PICOTCPDIR?=../../../picotcp
EXTRAOBJ=wrapper.o
PICOBUILD=picobuild
INC=-I $(PICOBUILD)/include
CFLAGS=-Wall -fPIC
CC=gcc

all: $(TARGET)

$(TARGET): $(PICOBUILD) $(EXTRAOBJ)
	$(CC) -shared -o $(TARGET) $(EXTRAOBJ) $(PICOBUILD)/lib/*.o $(PICOBUILD)/modules/*.o

$(PICOBUILD):
	make -C $(PICOTCPDIR) TUN=1 ARCH=shared
	cp -r $(PICOTCPDIR)/build $(PICOBUILD)

.c.o: 
	$(CC) -c $(CFLAGS) $(INC) $< -o $@

clean:
	rm -rf $(TARGET) $(EXTRAOBJ) $(PICOBUILD)
