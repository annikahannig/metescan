#ifndef UART_H
#define UART_H

#include "config.h"

#define BAUD 19200UL

// calculate baud
#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)
#define BAUD_REAL (F_CPU/(16*(UBRR_VAL+1)))
#define BAUD_ERROR ((BAUD_REAL*1000)/BAUD)

#if ((BAUD_ERROR<990) || (BAUD_ERROR>1010))
#error Error in baudrate > 0.1
#endif

#define UART_BUFFER_SIZE 80

#define UART_ECHO 0
void USART_init();
void USART_writeln(const char*);
void USART_puts(const char*);
void USART_tx(const unsigned char);

#endif

