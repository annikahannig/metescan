#ifndef PCF8574_H
#define PCF8574_H


#include <avr/io.h>


void PCF8574_init (void);

unsigned char PCF8574_send_start (void);

void PCF8574_send_stop (void);

unsigned char PCF8574_send_add_rw (unsigned char address, unsigned char rw);

unsigned char PCF8574_send_byte (unsigned char byte);

unsigned char PCF8574_read_byte (void);

extern unsigned char PCF8574_get_inputs (unsigned char address);

extern void PCF8574_set_outputs (unsigned char address, unsigned char byte);

#endif
