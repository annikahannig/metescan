#include "PCF8574.h"

/*
 * Original sourcecode from:
 * https://www.mikrocontroller.net/articles/Port-Expander_PCF8574
 * http://www.mikrocontroller.net/mc-project/Pages/Projekte/ICs/Port%20Expander/Portexpander%20Beispiel.zip
 */

void PCF8574_init (void)
{
  TWBR = 0x10;
}


unsigned char PCF8574_send_start (void)
{
	/*writing a one to TWINT clears it, TWSTA=Start, TWEN=TWI-enable*/
	TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN);
	/*wait, until start condition has been sent --> ACK*/
	while (!(TWCR & (1<<TWINT)));
	return TWSR;
}


void PCF8574_send_stop (void)
{
	/*writing a one to TWINT clears it, TWSTO=Stop, TWEN=TWI-enable*/
	TWCR = (1<<TWINT) | (1<<TWSTO) | (1<<TWEN);
}


unsigned char PCF8574_send_add_rw (uint8_t address, unsigned char rw)
{
	/* 
   * address can be 0 .. 8; rw=0 --> write, rw=1 --> read
   * default addr is 0x3F (PCF8574A)
   */
	uint8_t addr_byte = 0;
	/*shift address one bit left*/
	addr_byte = address << 1;
	/*set RW-Bit, if necessary*/
	addr_byte |= rw;
	/*0b0100xxx0 --> address of Expander*/
	// addr_byte |= 0b01000000;

  // 0b0111 for PCF8574A
	addr_byte |= 0b01110000;

	/*TWDR contains byte to send*/
	TWDR = addr_byte;
	/*send content of TWDR*/
	TWCR = (1<<TWINT) | (1<<TWEN);
	/*wait, until address has been sent --> ACK*/
	while (!(TWCR & (1<<TWINT)));
	return TWSR;
}


unsigned char PCF8574_send_byte(unsigned char byte)
{
	/*TWDR contains byte to send*/
	TWDR = byte;
	/*send content of TWDR*/
	TWCR = (1<<TWINT) | (1<<TWEN);
	/*wait, until byte has been sent --> ACK*/
	while (!(TWCR & (1<<TWINT)));
	return TWSR;
}


unsigned char PCF8574_read_byte (void)
{
	/*send content of TWDR; TWEA = enable ACK*/
	TWCR = (1<<TWINT) | (1<<TWEA) | (1<<TWEN);
	/*wait, until byte has been received --> ACK*/
	while (!(TWCR & (1<<TWINT)));
	return TWDR;
}


  unsigned char PCF8574_get_inputs(uint8_t address)
{
	PCF8574_init ();
	PCF8574_send_start ();
	PCF8574_send_add_rw (address, 1);
	unsigned char input = PCF8574_read_byte ();
	PCF8574_send_stop ();
	return input;
}


void PCF8574_set_outputs (uint8_t address, unsigned char byte)
{
	PCF8574_init ();
	PCF8574_send_start ();
	PCF8574_send_add_rw (address, 0);
	PCF8574_send_byte (byte);
	PCF8574_send_stop ();
}

