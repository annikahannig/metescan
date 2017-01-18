
#include "config.h"
#include <util/delay.h>

#include "lcd.h"
#include "pcf8574.h"

void LCD_write(uint8_t flags, uint8_t data)
{
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
  LCD_write(0x00, (data>>4));
  LCD_write(0x00, data);
}


void LCD_data(unsigned char data)
{
  LCD_write(LCD_RS, (data>>4));
  LCD_write(LCD_RS, data);
}


void LCD_clear()
{
  LCD_command(LCD_CLEAR);
  _delay_ms(15);
}

void LCD_init()
{
  // Wait > 40 ms after powerup
  _delay_ms(100);

  LCD_command(LCD_FN_8BIT); // 0x03
  _delay_ms(5);

  LCD_command(LCD_FN_8BIT); // 0x03
  _delay_ms(1);

  LCD_command(LCD_FN_8BIT); // 0x03
  _delay_ms(1);

  LCD_command(LCD_FN_4BIT); // 0x02
  _delay_ms(3);

  // 2 lines
  LCD_command(LCD_FN|LCD_FN_2LINE);
  _delay_ms(1);
  LCD_command(LCD_CTRL|LCD_CTRL_ON);
  _delay_ms(1);
  LCD_command(LCD_ENTRY|LCD_ENTRY_LEFT);
  _delay_ms(1);
  LCD_clear();
}


void LCD_set_cursor(uint8_t x, uint8_t y)
{
  uint8_t tmp;

  switch (y) {
    case 0: tmp=0x80+0x00+x; break;
    case 1: tmp=0x80+0x40+x; break;
    case 2: tmp=0x80+0x14+x; break;
    case 3: tmp=0x80+0x54+x; break;
    default: return;
  }
  LCD_command(tmp);
}


void LCD_string(char *data)
{
    while(*data) {
        LCD_data(*data);
        data++;
    }
}
