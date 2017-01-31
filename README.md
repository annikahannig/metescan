
MeteScan
========


This project is divided into two parts:
* The MeteScan python client
* The firmware for use with an ATMEGA 328 


--

The Client interacts with the Mete-API,
awaits user input from serial port (keys) and 
stdin (barcode scanner).

Requires asyncio, python3

## Usage

    usage: metescan.py [-h] -t API_TOKEN -m METE_HOST

    --api-token=API_TOKEN
    --mete-host=METE_HOST

    --verify-ca-bundle=/path/to/certificate_bundle.pem

    --device=/dev/tty.usbmodem1411
    --baud-rate=19200

Remember to always use https.


