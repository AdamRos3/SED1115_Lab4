# Uses serial blocking input given in announcement

from machine import Pin, UART
import time
import uasyncio as asyncio

# Initialize UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1) 

# Configure button input with internal pull-up
blocking_button = Pin(13, Pin.IN, Pin.PULL_DOWN)
# Will simulate message being sent from other pico for self testing
sim_button = Pin(11, Pin.IN, Pin.PULL_DOWN)

data_to_send = "Button pressed!"
print("Press the button to send message over UART")
blocking_prev_state = 0
sim_prev_state = 0

while True:
    blocking_current_state = blocking_button.value()
    sim_current_state = sim_button.value()

    # Detect button press (HIGH to LOW)
    if (blocking_prev_state == 1 and blocking_current_state == 0):
        # get (blocking) user input
        data_to_send = input("Data to send? ")
        uart.write(data_to_send.encode('utf-8'))
        print("Message sent: <", data_to_send.strip(), ">")

        # Debounce delat
        time.sleep(0.3)
    
    # Detect button press (HIGH to LOW)
    if (sim_prev_state == 1 and sim_current_state == 0):
        # send message to pico
        uart.write("Message from other pico")

        time.sleep(0.3)

    blocking_prev_state = blocking_current_state
    sim_prev_state = sim_current_state
    time.sleep(0.01)

    # Check for any incoming UART data
    if (uart.any()):
        data = uart.read()
        if data:
            print("Recevied:", data.decode('utf-8').strip())
            print("Press the button again to send another message over UART")
        else:
            print("Null message recevied")