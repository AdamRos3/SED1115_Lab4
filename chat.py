# Uses serial blocking input given in announcement
'''
Uses serial blocking input given in announcement
Although you can recieve multiple messages without hanging,
when in input mode, no messages can be recieved
'''

from machine import Pin, UART
import time

# Keep alive variables
tag = "#TAG#"
interval_ms = 10
timeout_ms = 1000
last_recieved = (time.time() * 1000)

# Initialize UART for internal use
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1) 

# Configure button input with internal pull-up
blocking_button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# Will simulate message being sent from other pico for self testing
sim_button = Pin(11, Pin.IN, Pin.PULL_DOWN)

data_to_send = "Button pressed!"
print("Press Westbound button to send message over UART")
print("Press Eastbound button to simulate sending message over UART to device")
print()

blocking_prev_state = 0
sim_prev_state = 0

while True:
    current_time = (time.time() * 1000)
    message_sent = False

    blocking_current_state = blocking_button.value()
    sim_current_state = sim_button.value()

    # Detect button press (HIGH to LOW)
    if (blocking_prev_state == 1 and blocking_current_state == 0):
        # get (blocking) user input
        data_to_send = input("Data to send? ")
        current_time = (time.time() * 1000)

        uart.write(data_to_send.encode('utf-8'))
        message_sent = True
        
        print("Message sent: <", data_to_send.strip(), ">")
        
        # Debounce delay
        time.sleep(0.3)
    blocking_prev_state = blocking_current_state

    # Detect button press (HIGH to LOW)
    if (sim_prev_state == 1 and sim_current_state == 0):
        # send message to pico
        uart.write("Message from other pico".encode('utf-8'))
        message_sent = True

        # Debounce delay
        time.sleep(0.3)
    sim_prev_state = sim_current_state

    # Check for any incoming UART data
    if (uart.any()):
        data = uart.read()
        if data:
            last_recieved = current_time
            data = data.decode('utf-8').strip()

            if data.startswith(tag):  
                pass
            else:              
                print("Recevied:", data)
        else:
            print("Null message recevied")

    if ((current_time - last_recieved) > interval_ms) and not message_sent:
        # sending keep alive, current time in milliseconds
        sending_time = time.localtime()
        message_time = (tag + str(sending_time))

        uart.write(message_time.encode('utf-8'))

    if ((current_time - last_recieved) > timeout_ms):
        print("Connection Timeout")
        break

    time.sleep(0.1)
    
print("... terminating connection")