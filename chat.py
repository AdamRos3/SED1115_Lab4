from machine import UART
from machine import Pin

uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1) 

while True:
    data = uart.read()
    
    if (data != None):
        print(data)

        message = input("Enter a message: ")
        uart.write(message + "\n")