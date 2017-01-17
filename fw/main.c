
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
    LCD_set_cursor(0,0);
    LCD_string("Test123");
    LCD_set_cursor(0,1);
    LCD_string("Test223");
    LCD_set_cursor(0,2);
    LCD_string("Test323");
    LCD_set_cursor(0,3);
    LCD_string("Test423");

    _delay_ms(1000);
    USART_writeln("cycle...");
  }
}



