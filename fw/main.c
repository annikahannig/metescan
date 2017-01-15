
/**
 * Matemat Firmware
 * ----------------
 *
 * Measure distance and write current distance for
 * each slot in serial console.
 *
 */

#include "config.h"

#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <string.h>
#include <stdio.h>

#include "uart.h"

#include "pcf8574.h"


#define LCD_I2C_ADDR 0x3F


/* 
 * wireing:
 *
 * P0 -> RS
 * P1 -> RW
 * P2 -> E
 *
 * P3 -> Backlight
 *
 * P4 -> D4
 * P5 -> D5
 * P6 -> D6
 * P7 -> D7
 *
 *  
 * Bits:
 *  D7 D6 D5 D4  BL EN RW RS
*/

#define LCD_RS (1<<0)
#define LCD_RW (1<<1)
#define LCD_EN (1<<2)
#define LCD_BL (1<<3)

#define LCD_D4 (1<<4)
#define LCD_D5 (1<<5)
#define LCD_D6 (1<<6)
#define LCD_D7 (1<<7)

#define LCD_OFF           0x00
#define LCD_ON            0x04
#define LCD_CLEAR         0x01
#define LCD_CURSOR_HOME   0x02

#define LCD_FN_8BIT       0x03
#define LCD_FN_4BIT       0x02

#define LCD_FN_5x8        0x00
#define LCD_FN_5x10       0x04
#define LCD_FN_2LINE      0x08


void LCD_write(uint8_t flags, uint8_t data) {

  uint8_t payload = (data<<4) | flags;

  // keep backlight on
  payload |= LCD_BL;

  // set output
  payload &= ~LCD_EN; // E low
  PCF8574_set_outputs(LCD_I2C_ADDR, payload);

  // pulse
  payload |= LCD_EN; // E high
  PCF8574_set_outputs(LCD_I2C_ADDR, payload);

  // pulse low
  payload &= ~LCD_EN; // E low
  PCF8574_set_outputs(LCD_I2C_ADDR, payload);
}


void LCD_command(unsigned char data)
{
  LCD_write(0x00, data);
}


void LCD_data(unsigned char data)
{
  LCD_write(LCD_RS, data);
}


void LCD_init() {

  // Wait > 40 ms after powerup
  _delay_ms(42);

  // Enable backlight
  PCF8574_set_outputs(LCD_I2C_ADDR, LCD_BL);

  // Display initialization
  _delay_ms(10);

  LCD_command(LCD_FN_8BIT);
  _delay_ms(5);

  LCD_command(LCD_FN_8BIT);
  _delay_ms(1);

  LCD_command(LCD_FN_8BIT);
  _delay_ms(1);

  LCD_command(LCD_FN_4BIT);
  _delay_ms(1);

  // 2 lines
  LCD_command(LCD_FN_2LINE);
  _delay_ms(1);

  // Display on
  LCD_command(LCD_ON);

  LCD_command(LCD_CLEAR);
  _delay_ms(1);
  LCD_command(LCD_CURSOR_HOME);
  _delay_ms(1);
}


void LCD_set_cursor(uint8_t x, uint8_t y)
{
  uint8_t tmp;

  switch (y) {
    case 0: tmp=0x80+0x00+x; break;
    case 1: tmp=0x80+0x40+x; break;
    case 2: tmp=0x80+0x10+x; break;
    case 3: tmp=0x80+0x50+x; break;
    default: return;
  }
  LCD_command(tmp);
}


int main(void) {

  // Setup UART
  USART_init();

  // Setup LCD
  LCD_init();

  // Enable interrupts
  sei();

  USART_writeln("Starting...");

  for(;;) {

    _delay_ms(1000);

    _delay_ms(1000);
    USART_writeln("cycle...");

  }
}



