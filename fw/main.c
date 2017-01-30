
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
#include "lcd.h"


#define RX_CMD(buf, x) (strncmp(buf, x, sizeof(x)-1)==0)

/*
 * Print welcome and version
 */
void _cmd_helo()
{
  USART_writeln("METESCAN");
  USART_writeln("VERSION 1.0.0");
  USART_writeln("READY");
}


int main(void)
{
  char *cmd;

  // Setup UART
  USART_init();

  // Setup LCD
  LCD_init();

  // Enable interrupts
  sei();

  for(;;) {
    cmd = USART_read();
    if (cmd == NULL) {
      _delay_ms(10);
      continue;
    }

    if RX_CMD(cmd, "HELO") {
      _cmd_helo();
    }
    else if RX_CMD(cmd, "CLR") {
      LCD_clear();
    }
    else if RX_CMD(cmd, "0 ") { // Set row 0
      LCD_set_cursor(0,0);
      LCD_string(cmd+2);
    }
    else if RX_CMD(cmd, "1 ") { // Set row 1
      LCD_set_cursor(0,1);
      LCD_string(cmd+2);
    }
    else if RX_CMD(cmd, "2 ") { // Set row 2
      LCD_set_cursor(0,2);
      LCD_string(cmd+2);
    }
    else if RX_CMD(cmd, "3 ") { // Set row 3
      LCD_set_cursor(0,3);
      LCD_string(cmd+2);
    }
  }
}


