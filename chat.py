from machine import Pin, UART
import time
import uasyncio as asyncio

# Initialize UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1) 

# Configure button input with internal pull-up
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

data_to_send = "Button pressed!"
print("Press the button to send message over UART")
prev_state = 0

while True:
    current_state = button.value()

    # Detect button press (HIGH to LOW)
    if (prev_state == 1 and current_state == 0):
        # get (blocking) user input
        data_to_send = input("Data to send? ")
        uart.write(data_to_send.encode('utf-8'))
        print("Message sent: <", data_to_send.strip(), ">")

        # Debounce delat
        time.sleep(0.3)
    
    prev_state = current_state
    time.sleep(0.01)

    # Check for any incoming UART data
    if (uart.any()):
        data = uart.read()
        if data:
            print("Recevied:", data.decode('utf-8').strip())
            print("Press the button again to send another message over UART")
        else:
            print("Null message recevied")