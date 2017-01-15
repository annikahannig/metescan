
#include "uart.h"

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>


volatile uint8_t _uart_string_ready = 0;
volatile uint8_t _uart_string_length = 0;
volatile char    _uart_string_buffer[UART_BUFFER_SIZE] = "";

/**
 * UART receive interrupt
 */
ISR( USART_RX_vect )
{
    static uint8_t count;
    unsigned char c = UDR0;

    if( _uart_string_ready == 0 ) {
      if( c == '\r' ) {
      }
      else if( c != '\n' &&
          count < UART_BUFFER_SIZE - 1 ) {
          // append char to string
          _uart_string_buffer[count] = c;
          count++;
      }
      else {
          // terminate string
          _uart_string_buffer[count] = '\0';
          _uart_string_length = count;
          count = 0;
          _uart_string_ready = 1;
      }
    }

  // echo back
  #if UART_ECHO == 1
      UDR0 = c;
  #endif
}

/**
 * Transmit a single char
 */
void USART_tx(const unsigned char data)
{
    /* Wait for empty transmit buffer */
    while(!(UCSR0A & (1<<UDRE0))) {
        // do_nothing() tm
    };

    /* Put data into buffer, sends the data */
    UDR0 = data;
}

/**
 * Send a string
 */
void USART_puts(const char* s)
{
    while (*s)
    {
        USART_tx(*s);
        s++;
    }
}

/**
 * Write a single line
 */
void USART_writeln(const char *s)
{
    USART_puts(s);
    USART_tx('\n');
    USART_tx('\r');
}

/**
 * Wait until string ready,
 * return pointer to string buffer
 */
char* USART_read()
{
	if( _uart_string_ready == 1 ) {
		_uart_string_ready = 0;
		return (char*)_uart_string_buffer;
	}

	return NULL;
}

/**
 * Initialize UART
 */
void USART_init()
{
    /* Set baud rate */
    UBRR0H = (unsigned char)(UBRR_VAL>>8);
    UBRR0L = (unsigned char)(UBRR_VAL & 0xff);

    UCSR0A &= ~(1<<U2X0); // 1x data rate
    UCSR0C = (1<<UCSZ01)|(3<<UCSZ00);
    /* Enable transmitter only */
    UCSR0B |= (1<<TXEN0);
}



