
# Makefile inspired from jasegs Klingel.

CC=avr-gcc

DEVICE=atmega328p

CFLAGS = -g2 -mmcu=$(DEVICE) -Os
CFLAGS+= -Os -ffunction-sections -fdata-sections -fpack-struct
CFLAGS+= -fno-move-loop-invariants -fno-tree-scev-cprop
CFLAGS+= -fno-inline-small-functions
CFLAGS+= -Wall -Wno-pointer-to-int-cast


LDFLAGS = -Wl,-u,vfprintf -lprintf_flt


# OS Detection
UNAME=$(shell uname)
ifeq ($(UNAME), Darwin)
  PROG_PRT=cu.usbmodem1421
else
  PROG_PRT=ttyUSB1
endif

all: main.elf

uart.o: uart.c
	$(CC) $(CFLAGS) -c -o uart.o uart.c

lcd.o: lcd.c
	$(CC) $(CFLAGS) -c -o lcd.o lcd.c

pcf8574.o: pcf8574.c
	$(CC) $(CFLAGS) -c -o pcf8574.o pcf8574.c

main.o: main.c
	$(CC) $(CFLAGS) -c -o main.o main.c

main.elf: uart.o main.o pcf8574.o lcd.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o main.elf main.o uart.o pcf8574.o lcd.o
	avr-objcopy  -O ihex -R .eeprom main.elf main.hex

flash:	main.elf
	sudo avrdude -c arduino -P /dev/$(PROG_PRT) -b 115200 -p $(DEVICE) -U flash:w:main.hex



clean:
	rm -f *.o
	rm -f *.elf
	rm -f *.map
	rm -f *.hex

.PHONY: clean

