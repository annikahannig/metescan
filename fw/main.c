
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

#define BT_PORT PORTB
#define BT_PIN  PINB
#define BT_DDR  DDRB

#define BT_CANCEL (1<<PB0)
#define BT_CANCEL_MSK (1<<PCIE0)
#define BT_CANCEL_INT (1<<PCINT0)


/*
 * Input handler
 */
void INPUT_init()
{
  BT_DDR &= ~BT_CANCEL; // use as input
  BT_PORT &= ~BT_CANCEL; // no internal pullups

  // setup interrupt registers
  PCICR |= BT_CANCEL_MSK; // enable PCMSK0 (PCINT0)
  PCMSK0 |= BT_CANCEL_INT;

  // setup timer
  TCCR1A = 0x00;
  TCCR1B = (1<<CS12) | (1<<CS10); // Prescaler: 1024

}

// Input interrupt handler
ISR(PCINT0_vect)
{
  if (BT_PIN & BT_CANCEL) { // BT UP
    int pulse_length = TCNT1;
    if (pulse_length > 60) {
      USART_writeln("BT_CANCEL_UP");
    }
  }
  else {
    TCNT1=0; // reset timer
  }
}




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

  // Setup button input
  INPUT_init();

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

    cli();

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

    sei();
  }
}


