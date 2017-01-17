#ifndef LCD_H
#define LCD_H

#include <stdint.h>

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

#define LCD_CTRL          0x08

#define LCD_CTRL_OFF      0x00
#define LCD_CTRL_ON       0x04

#define LCD_CLEAR         0x01
#define LCD_CURSOR_HOME   0x02

#define LCD_FN_8BIT       0x03
#define LCD_FN_4BIT       0x02

#define LCD_FN            0x20
#define LCD_FN_5x8        0x00
#define LCD_FN_5x10       0x04
#define LCD_FN_2LINE      0x08
#define LCD_FN_1LINE      0x00

#define LCD_ENTRY         0x04
#define LCD_ENTRY_LEFT    0x02


void LCD_write(uint8_t flags, uint8_t data);
void LCD_command(unsigned char data);
void LCD_data(unsigned char data);
void LCD_string(char *data);
void LCD_set_cursor(uint8_t x, uint8_t y);
void LCD_clear();
void LCD_init();

#endif

